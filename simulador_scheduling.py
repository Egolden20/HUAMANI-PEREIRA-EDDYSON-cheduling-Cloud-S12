"""Laboratorio de scheduling cloud (simulación determinista, sin crear VMs reales)."""
import csv, json, random, os
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def save_csv(name, rows, fields):
    with (ROOT/name).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def schedule_fixed(jobs, n=3, order=None, mode='cyclic'):
    jobs_by_id={j['id']:j for j in jobs}; order=order or list(jobs_by_id)
    loads=[0]*n; rows=[]
    for index,jid in enumerate(order):
        j=jobs_by_id[jid]
        machine=index%n if mode=='cyclic' else min(range(n),key=lambda k:(loads[k],k))
        start=loads[machine]; duration=j['duration']; loads[machine]+=duration
        rows.append(dict(job=jid,vm=f'VM{machine+1}',start=start,end=loads[machine],duration=duration))
    return loads,rows

def summary(loads,rows):
    makespan=max(loads); return {'makespan':makespan,'total_work':sum(loads),'mean_wait':round(sum(r['start'] for r in rows)/len(rows),3),'utilization_pct':round(100*sum(loads)/(len(loads)*makespan),2)}

JOBS=[dict(id=f'J{i}',duration=t) for i,t in enumerate([12,4,8,3,10,6,2,7],1)]
order_sjf=[j['id'] for j in sorted(JOBS,key=lambda j:(j['duration'],j['id']))]
rr_l,rr_r=schedule_fixed(JOBS)
sjf_l,sjf_r=schedule_fixed(JOBS,order=order_sjf,mode='earliest')
opt_order=[('VM1',['J1','J6']),('VM2',['J5','J4','J2']),('VM3',['J3','J8','J7'])]
opt_l=[];opt_r=[]
for vm,ids in opt_order:
    at=0
    for jid in ids:
        duration=next(j['duration'] for j in JOBS if j['id']==jid)
        opt_r.append(dict(job=jid,vm=vm,start=at,end=at+duration,duration=duration));at+=duration
    opt_l.append(at)

# Escenario propio, diseñado siguiendo la guía de laboratorio: 50 jobs / 5 VM heterogéneas.
# Duración en segundos = tamaño del trabajo (millones de instrucciones) / velocidad (MIPS).
rng=random.Random(20261030)
vm_speed=[1000,1500,2000,2500,3000]
job_mi=[rng.randint(8000,40000) for _ in range(50)]

def fcfs():
    loads=[0.0]*5;rows=[]
    for i,mi in enumerate(job_mi):
        vm=min(range(5),key=lambda k:(loads[k],k))
        start=loads[vm];duration=mi/vm_speed[vm];loads[vm]+=duration
        rows.append(dict(job=f'T{i+1:02d}',vm=f'VM{vm+1}',size_mi=mi,start=round(start,3),end=round(loads[vm],3),duration=round(duration,3)))
    return loads,rows

def minmin():
    loads=[0.0]*5;rows=[]; pending=set(range(50))
    while pending:
        # el mejor recurso para cada tarea, luego seleccionar la menor terminación global
        best=[]
        for i in pending:
            k=min(range(5),key=lambda v:(loads[v]+job_mi[i]/vm_speed[v],v))
            best.append((loads[k]+job_mi[i]/vm_speed[k],i,k))
        _,i,k=min(best,key=lambda z:(z[0],z[1],z[2]))
        start=loads[k];duration=job_mi[i]/vm_speed[k];loads[k]+=duration
        rows.append(dict(job=f'T{i+1:02d}',vm=f'VM{k+1}',size_mi=job_mi[i],start=round(start,3),end=round(loads[k],3),duration=round(duration,3)))
        pending.remove(i)
    return loads,rows

fc_l,fc_r=fcfs(); mm_l,mm_r=minmin()
def scenario2_summary(loads,rows):
    cmax=max(loads)
    return {'makespan_s':round(cmax,3),'mean_wait_s':round(sum(r['start'] for r in rows)/len(rows),3),'vm_busy_s':[round(x,3) for x in loads], 'avg_vm_active_pct':round(100*sum(loads)/(5*cmax),2),'vm_utilization_pct':[round(100*x/cmax,2) for x in loads]}

result={'eval':{'rr':{'loads':rr_l,**summary(rr_l,rr_r)},'sjf':{'loads':sjf_l,**summary(sjf_l,sjf_r)},'optimized':{'loads':opt_l,**summary(opt_l,opt_r)},'sjf_order':order_sjf},'laboratorio':{'vm_mips':vm_speed,'fcfs':scenario2_summary(fc_l,fc_r),'minmin':scenario2_summary(mm_l,mm_r),'seed':20261030}}
(ROOT/'resultados.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
save_csv('dataset_50_tareas.csv',[{'trabajo':f'T{i+1:02d}','tamano_mi':mi} for i,mi in enumerate(job_mi)],['trabajo','tamano_mi'])
for name,rows in [('evaluacion_rr.csv',rr_r),('evaluacion_sjf.csv',sjf_r),('evaluacion_optimizado.csv',opt_r)]:save_csv(name,rows,['job','vm','start','end','duration'])
for name,rows in [('laboratorio_fcfs.csv',fc_r),('laboratorio_minmin.csv',mm_r)]:save_csv(name,rows,['job','vm','size_mi','start','end','duration'])
plt.rcParams.update({'font.size':10})
fig,ax=plt.subplots(figsize=(9,4));names=['RR','SJF + VM libre antes','Balanceo optimizado'];values=[max(rr_l),max(sjf_l),max(opt_l)]; bars=ax.bar(names,values,color=['#64748b','#0f766e','#2563eb']);ax.bar_label(bars,padding=4,fmt='%.0f');ax.set_ylim(0,max(values)+5);ax.set_ylabel('Makespan (min)');ax.set_title('Evaluación: 8 trabajos / 3 VM homogéneas');fig.tight_layout();fig.savefig(ROOT/'comparacion_evaluacion.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4));names=['FCFS','Min-Min'];values=[max(fc_l),max(mm_l)];bars=ax.bar(names,values,color=['#64748b','#2563eb']);ax.bar_label(bars,padding=4,fmt='%.2f');ax.set_ylim(0,max(values)*1.18);ax.set_ylabel('Makespan (seg)');ax.set_title('Laboratorio: 50 trabajos / 5 VM heterogéneas');fig.tight_layout();fig.savefig(ROOT/'comparacion_laboratorio.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4));width=.35;x=list(range(5));ax.bar([k-width/2 for k in x],fc_l,width,label='FCFS',color='#64748b');ax.bar([k+width/2 for k in x],mm_l,width,label='Min-Min',color='#2563eb');ax.set_xticks(x,[f'VM{i+1}' for i in x]);ax.set_ylabel('Tiempo ocupado (seg)');ax.set_title('Carga acumulada por máquina virtual');ax.legend();fig.tight_layout();fig.savefig(ROOT/'cargas_laboratorio.png',dpi=160);plt.close(fig)
print(json.dumps(result,indent=2,ensure_ascii=False))
