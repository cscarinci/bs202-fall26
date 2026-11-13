import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title='BS202 • Lecture 20 • Confidence intervals', css_file="bs202.css")

@app.cell(hide_code=True)
def _():
    import math

    import marimo as mo
    import matplotlib
    import numpy as np
    from matplotlib.figure import Figure

    # Figures use the same Computer Modern typeface as the text
    matplotlib.rcParams.update({"font.size": 14, "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"], "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True, "axes.unicode_minus": False, "savefig.format": "svg"})

    return Figure, math, mo, np

@app.cell(hide_code=True)
def _(mo):
    # ---- Building blocks shared by all lectures -------------------------
    # Palette with fixed roles (figures only; text carries no colour):
    #   BLUE   the primary object (the point, the chosen vector, the main curve)
    #   RED    the second object it is compared with
    #   GREEN  a derived quantity (tangent vector, gradient, mean)
    #   GREY   reference geometry (guides, unit circle, reference curves)
    #   LIGHT  fills and grids
    BLUE, RED, GREEN, GREY, LIGHT = "#3f5f8f", "#a8554c", "#4f7f5c", "#9a9a9a", "#e3ebf4"
    # Figure widths: HALF sits beside text or in a pair
    HALF = 3.6

    def header(document, date, running=""):
        """Course header, as on the exercise sheets and exams."""
        return mo.Html(
            f"""
    <div class="bs-head">
      <div class="bs-running">BS202 &bull; {running}</div>
      <div class="bs-title">Introduction to Probability<br>and Mathematical Statistics</div>
      <div class="bs-inst">Daegu Gyeongbuk Institute of Science and Technology<br>School of Undergraduate Studies</div>
      <div class="bs-meta">
        <b>Document</b><span>{document}</span><b>Course</b><span>BS202a</span>
        <b>Week</b><span>{date.removeprefix('Week ')}</span><b>Instructor</b><span>Professor Scarinci</span>
      </div>
    </div>
    """
        )

    def _statement(label, title, body):
        head = f"**{label}" + (f" ({title})" if title else "") + ".**"
        return mo.md(head + "\n\n" + body).style({"border-left": f"2px solid {BLUE}", "padding-left": "1rem"})

    def definition(body, title=""):
        return _statement("Definition", title, body)

    def theorem(body, title=""):
        return _statement("Theorem", title, body)

    def table(rows):
        """Fixed-label readout table: rows are (label, value) pairs of markdown strings."""
        _md = mo.md("\n".join(["| | |", "|:--|:--|"] + [f"| {k} | {v} |" for k, v in rows]))
        return mo.Html(f'<div class="readout">{_md.text}</div>')

    def corollary(body, title=""):
        return _statement("Corollary", title, body)

    def arrow(ax, tail, tip, color, label=None, at_tip=False, lw=1.4, **kw):
        """Draw the vector from `tail` to `tip` on a 2D axis, labelled at its middle or its tip.
        The head is sized in points from the line width (length 4 lw, full width 2.5 lw), never in data units,
        so arrows look alike in every figure whatever its axis range."""
        ax.annotate(
            "",
            xy=tip,
            xytext=tail,
            arrowprops={"arrowstyle": f"-|>,head_length={4 * lw:g},head_width={1.25 * lw:g}", "mutation_scale": 1, "color": color, "lw": lw, "shrinkA": 0, "shrinkB": 0, **kw},
        )
        if label:
            pos = tip if at_tip else ((tail[0] + tip[0]) / 2, (tail[1] + tip[1]) / 2)
            ax.annotate(label, pos, textcoords="offset points", xytext=(6, 6), color=color, fontsize=13)

    return corollary, LIGHT, BLUE, GREEN, GREY, HALF, RED, arrow, definition, header, table, theorem

@app.cell(hide_code=True)
def _(header):
    header("Lecture 20","Week 12","Lecture 20 • Confidence intervals")
    return


@app.cell(hide_code=True)
def _(BLUE, GREEN, GREY, LIGHT, RED, Figure, arrow, np):
    def lecture_sketch(kind, value=0.5):
        fig = Figure(figsize=(6.6, 3.5))
        ax = fig.add_axes((0.07, 0.08, 0.85, 0.84))
        ax.set_aspect('equal')
        ax.axis('off')
        def label(p, text, color='black', offset=(5,5), ha='left', va='bottom'):
            ax.annotate(text,p,xytext=offset,textcoords='offset points',color=color,fontsize=13,ha=ha,va=va,zorder=10,clip_on=False)
        def axes(xlim,ylim,x='$x$',y='$y$'):
            ax.set_xlim(*xlim);ax.set_ylim(*ylim)
            arrow(ax,(xlim[0],0),(xlim[1]-0.1,0),'black',lw=0.9)
            arrow(ax,(0,ylim[0]),(0,ylim[1]-0.1),'black',lw=0.9)
            label((xlim[1]-0.1,0),x,offset=(0,-18),ha='right')
            label((0,ylim[1]-0.1),y,offset=(-12,0))
        if kind=='partition':
            ax.set_xlim(-0.4,5.5);ax.set_ylim(-0.6,0.7)
            arrow(ax,(-0.2,0),(5.3,0),'black',lw=0.9)
            for i in range(6):
                ax.plot([i,i],[-0.05,0.05],color=GREY,lw=1)
            for i in range(5):
                ax.plot(i+0.4,0,'o',color=BLUE,zorder=5,ms=4)
            for x,t in [(0,'$a=a_1$'),(1,'$b_1=a_2$'),(4,'$a_N$'),(5,'$b_N=b$')]:label((x,0),t,offset=(0,14),ha='center')
            for x,t in [(0.4,'$t_1$'),(1.4,'$t_2$'),(4.4,'$t_N$')]:label((x,0),t,BLUE,offset=(0,-24),ha='center')
            fig.set_size_inches(6.6,1.6)
        elif kind=='rectangle':
            axes((-0.4,4.0),(-0.4,2.9))
            ax.fill([0.7,3,3,0.7],[0.6,0.6,2.2,2.2],color=LIGHT)
            ax.plot([0.7,3,3,0.7,0.7],[0.6,0.6,2.2,2.2,0.6],color=BLUE,lw=1.4)
            for x,t in [(0.7,'$a$'),(3,'$b$')]:
                ax.plot([x,x],[0,2.2],':',color=GREY);label((x,0),t,offset=(0,-18),ha='center')
            for y,t in [(0.6,'$c$'),(2.2,'$d$')]:
                ax.plot([0,3],[y,y],':',color=GREY);label((0,y),t,offset=(-15,0))
            label((2.7,1.3),'$R$',BLUE)
        elif kind in ('simple_regions','green_y','green_x'):
            # Vertical/horizontal slices and the four oriented boundary pieces.
            def region(ax, swap=False, orient=False):
                x=np.linspace(0.7,3.2,180);lo=0.8+0.18*np.sin(4*x);hi=2.2+0.2*np.sin(3*x)
                conv=lambda x,y:(y,x) if swap else (x,y)
                ax.fill(*conv(np.r_[x,x[::-1]],np.r_[lo,hi[::-1]]),color=LIGHT)
                ax.plot(*conv(x,lo),color=BLUE,lw=1.4);ax.plot(*conv(x,hi),color=BLUE,lw=1.4)
                for i in (0,-1):ax.plot(*conv([x[i],x[i]],[lo[i],hi[i]]),color=RED,lw=1.4)
                if orient:
                    for xs,ys,rev,c in [(x,lo,False,BLUE),(x,hi,True,BLUE)]:
                        a,b=85,95
                        if rev:a,b=b,a
                        tail,tip=conv(xs[a],ys[a]),conv(xs[b],ys[b])
                        if swap:tail,tip=tip,tail
                        arrow(ax,tail,tip,c,mutation_scale=2.5)
                    for i,sign in [(0,-1),(-1,1)]:
                        mid=(lo[i]+hi[i])/2
                        a,b=conv(x[i],mid-0.13*sign),conv(x[i],mid+0.13*sign)
                        if swap:a,b=b,a
                        arrow(ax,a,b,RED,mutation_scale=2.5)
                else:
                    k=85
                    ax.plot(*conv([x[k],x[k]],[lo[k],hi[k]]),color=GREEN,lw=1.5)
                    for yy,txt in [(lo[k],r'$\psi_1(y)$' if swap else r'$\varphi_1(x)$'),(hi[k],r'$\psi_2(y)$' if swap else r'$\varphi_2(x)$')]:
                        ax.plot(*conv([0,x[k]],[yy,yy]),':',color=GREY,lw=0.7)
                        ax.plot(*conv(x[k],yy),'o',color=GREEN,zorder=5,ms=3)
                        label(conv(0,yy),txt,GREEN,offset=(0,-23) if swap else (-9,0),ha='center' if swap else 'right')
                    label(conv(x[k],0),'$y$' if swap else '$x$',GREEN,offset=(-14,0) if swap else (0,-20),ha='center')
                if swap:
                    label((1.0,3.4),r'$x=\psi_1(y)$',BLUE,offset=(0,0),ha='center')
                    label((2.7,3.4),r'$x=\psi_2(y)$',BLUE,offset=(0,0),ha='center')
                else:
                    label((1.6,0.25),r'$y=\varphi_1(x)$',BLUE,offset=(0,2),ha='center')
                    label((1.6,2.45),r'$y=\varphi_2(x)$',BLUE,offset=(0,2),ha='center')
                label(conv(2.4,1.4),'$D$',BLUE)
                for p,t in [(conv(0.7,0), '$c$' if swap else '$a$'),(conv(3.2,0),'$d$' if swap else '$b$')]:label(p,t,offset=(-14,0) if swap else (0,-20),ha='center')
            if kind=='simple_regions':
                fig=Figure(figsize=(7.4,3.5));ax=fig.add_axes((0.04,0.12,0.42,0.8));ax.axis('off');ax.set_aspect('equal')
                axes((-0.3,3.8),(-0.3,3.7));region(ax)
                ax=fig.add_axes((0.55,0.12,0.42,0.8));ax.axis('off');ax.set_aspect('equal')
                axes((-0.3,3.8),(-0.3,3.7));region(ax,True)
            else:
                axes((-0.3,3.9),(-0.3,3.9));region(ax,kind=='green_x',True)
        elif kind in ('parabola','parabola_boundary'):
            axes((-1.65,1.65),(-0.25,1.65));x=np.linspace(-1,1,240)
            ax.fill_between(x,x*x,1,color=LIGHT)
            ax.plot(x,x*x,color=BLUE,lw=1.4);ax.plot([-1,1],[1,1],color=RED,lw=1.4)
            label((0.8,0.5),r'$y=x^2$' if kind=='parabola' else r'$\vec C_1$',BLUE)
            label((-0.7,1.04),'$y=1$' if kind=='parabola' else r'$\vec C_2$',RED)
            label((-0.42,0.72),'$D$',BLUE)
            if kind=='parabola_boundary':
                arrow(ax,(0.4,0.16),(0.55,0.55**2),BLUE,mutation_scale=2.5);arrow(ax,(0.4,1),(0.15,1),RED,mutation_scale=2.5)
            else:
                y=value;ax.plot([-np.sqrt(y),np.sqrt(y)],[y,y],color=GREEN,lw=1.4)
        elif kind in ('line_integral','parallel_path'):
            ax.set_xlim(-0.3,5.8);ax.set_ylim(-0.5,3.1)
            t=np.linspace(0,4.8,200);y=0.3*t+0.35*np.sin(1.5*t)
            ax.plot(t,y,color=BLUE,lw=1.4)
            for x,text in [(0,r'$\gamma(a)$'),(4.8,r'$\gamma(b)$')]:
                p=(x,0.3*x+0.35*np.sin(1.5*x));ax.plot(*p,'o',color=BLUE,zorder=5,ms=4);label(p,text,offset=(0,-24),ha='center')
            if kind=='line_integral':
                p=np.array([2.,0.6+0.35*np.sin(3)])
                tangent=p+1.6*np.array([1.,0.3+0.525*np.cos(3)])
                arrow(ax,p,tangent,GREEN,lw=1.7,mutation_scale=2.2)
                label(tangent,r"$\gamma'(t)$",GREEN,offset=(5,-12),va='top')
                arrow(ax,p,p+[0.1,1.3],RED,lw=1.7,mutation_scale=2.2)
                label(p+[0.1,1.3],r'$\vec F(\gamma(t))$',RED,offset=(5,8))
                label(p,r'$\gamma(t)$',BLUE,offset=(0,-25),ha='center')
            else:
                for x,c,txt in [(0,BLUE,'$X_0$'),(2.2,RED,r'$X_{\gamma(t)}$'),(4.8,GREEN,r'$P^\gamma_{a,b}(X_0)$')]:
                    p=np.array([x,0.3*x+0.35*np.sin(1.5*x)])
                    tip=p+[-0.18+0.15*x,0.95]
                    arrow(ax,p,tip,c);label(tip,txt,c,offset=(0,7),ha='center')
        elif kind=='orientation':
            axes((-0.4,3.7),(-0.3,2.7));t=np.linspace(0,2*np.pi,240)
            x=1.7+1.05*np.cos(t);y=1.3+0.85*np.sin(t)
            ax.fill(x,y,color=LIGHT);ax.plot(x,y,color=BLUE,lw=1.4)
            for k in (25,145):arrow(ax,(x[k],y[k]),(x[k+10],y[k+10]),BLUE,mutation_scale=2.5)
            label((1.55,1.2),'$D$',BLUE);label((2.4,2.1),r'$\vec C$',BLUE)
        elif kind=='ellipse':
            axes((-2.8,2.8),(-1.8,1.8));t=np.linspace(0,2*np.pi,250)
            ax.fill(2*np.cos(t),np.sin(t),color=LIGHT);ax.plot(2*np.cos(t),np.sin(t),color=BLUE,lw=1.4)
            for p,txt,off,ha,va in [((2,0),'$a$',(7,5),'left','bottom'),((-2,0),'$-a$',(-7,5),'right','bottom'),((0,1),'$b$',(5,7),'left','bottom'),((0,-1),'$-b$',(5,-7),'left','top')]:
                label(p,txt,BLUE,offset=off,ha=ha,va=va)
        elif kind=='potential_rectangle':
            axes((-0.5,3.4),(-0.4,2.6));ax.fill([0,2.5,2.5,0],[0,0,1.7,1.7],color=LIGHT)
            arrow(ax,(0,0),(2.5,0),BLUE,mutation_scale=2.5);arrow(ax,(2.5,0),(2.5,1.7),BLUE,mutation_scale=2.5)
            arrow(ax,(2.5,1.7),(0,1.7),RED,mutation_scale=2.5);arrow(ax,(0,1.7),(0,0),RED,mutation_scale=2.5)
            for p,t,off,ha,va in [((0,0),'$(0,0)$',(-6,-7),'right','top'),((2.5,0),'$(x,0)$',(6,-7),'left','top'),((2.5,1.7),'$(x,y)$',(6,7),'left','bottom'),((0,1.7),'$(0,y)$',(-6,7),'right','bottom')]:
                label(p,t,offset=off,ha=ha,va=va)
            label((1,-0.3),r'$\vec C_1$',BLUE,offset=(0,-6));label((0.8,1.85),r'$\vec C_2$',RED);label((1.1,0.8),'$R$',BLUE)
        elif kind in ('fixed_interval','moving_interval'):
            fig.set_size_inches(6.6,1.7);ax.set_aspect('auto');ax.set_xlim(-10,110);ax.set_ylim(-0.6,0.7)
            arrow(ax,(-5,0),(105,0),'black',lw=0.9)
            centre=50 if kind=='fixed_interval' else value
            for x in (centre-19.6,centre+19.6):ax.plot([x,x],[-0.08,0.08],color=BLUE,lw=1.4)
            ax.plot([centre-19.6,centre+19.6],[0,0],color=BLUE,lw=2)
            mean=56 if kind=='fixed_interval' else value
            ax.plot(mean,0,'o',color=GREEN,zorder=5,ms=5);ax.plot(50,0,'o',color=RED,zorder=5,ms=4)
            for x,t,c in [(50,r'$\mu$',RED),(mean,r'$M_4$',GREEN)]:label((x,0),t,c,offset=(0,-26 if c==RED else 16),ha='center')
            for sign in (-1,1):label((centre+sign*19.6,0),('$\\mu' if kind=='fixed_interval' else '$M_4')+(' - ' if sign<0 else ' + ')+r'\varepsilon$',BLUE,offset=(0,16),ha='center')
        elif kind in ('schwarzschild_domain','static_clock','newton_force'):
            axes((-1.8,4.3),(-0.7,3.9),x='$r$',y=r'$\tau$' if kind=='newton_force' else '$t$')
            if kind=='static_clock':
                ax.plot([0.9,0.9],[-0.2,3.5],':',color=GREY)
                ax.plot([1.7,1.7],[-0.2,3.5],color=BLUE,lw=1.4)
                arrow(ax,(3,0.6),(3,3),GREEN)
                for p,t,c in [((0.9,0),'$2M$',GREY),((1.7,0),'$r_0$',BLUE),((3,0),'$r$',GREEN)]:label(p,t,c,offset=(0,-22),ha='center')
                for p,t in [((3,0.6),r'$\gamma(a)$'),((3,2.7),r'$\gamma(b)$')]:ax.plot(*p,'o',color=GREEN,zorder=5,ms=4);label(p,t,GREEN)
            else:
                for x in (-1.2,1.2):ax.plot([x,x],[-0.4,3.6],color=BLUE,lw=1.2)
                t=np.linspace(0,2*np.pi,160);ax.plot(1.2*np.cos(t),0.35*np.sin(t),color=BLUE,lw=1.2)
                label((1.2,0),'$r_0$',BLUE,offset=(0,-22));label((-1.2,-0.3),r'$\mathbb{S}^2$' if kind=='schwarzschild_domain' else r'$\sigma(\tau)=o+\tau e_0$',BLUE,offset=(-5,-20))
                if kind=='newton_force':
                    t=np.linspace(-0.3,3.5,140);r=2.1+0.6*np.sin(1.2*t);ax.plot(r,t,color=RED,lw=1.4)
                    arrow(ax,(2.7,1.3),(1.7,1.3),GREEN,r'$F(\gamma(\tau))$',at_tip=True)
                    label((2.5,3),r'$\gamma(\tau)$',RED)
                else:label((2.7,2.7),'$M$',BLUE)
        elif kind in ('newton_orbits','precession'):
            axes((-3,2) if kind=='newton_orbits' else (-2.6,2.6),(-2.4,2.4) if kind=='newton_orbits' else (-2.6,2.6),x='',y='');ax.plot(0,0,'o',color=GREY,zorder=5,ms=13)
            if kind=='newton_orbits':
                for e,c in [(0.55,BLUE),(1.,RED),(1.4,GREEN)]:
                    t=np.linspace(-np.pi,np.pi,1600);den=1+e*np.cos(t);ok=den>0.06;r=1/den[ok];t=t[ok]
                    xx,yy=r*np.cos(t),r*np.sin(t); visible=(xx>=-3)&(xx<=2)&(abs(yy)<=2.4)
                    ax.plot(np.where(visible,xx,np.nan),np.where(visible,yy,np.nan),color=c,lw=1.4,label=f'$e={e:g}$')
                ax.legend(loc='upper left',bbox_to_anchor=(1.0,1.0),fontsize=12,frameon=True,fancybox=False,edgecolor='#c8c8c8')
            else:
                fig.set_size_inches(6.6,4.4);ax.set_xlim(-2.6,2.6);ax.set_ylim(-2.6,2.6)
                t=np.linspace(0,16*np.pi/(1-3*value**2),6000);r=1/(1+0.55*np.cos((1-3*value**2)*t))
                ax.plot(r*np.cos(t),r*np.sin(t),color=BLUE,lw=1.4)
                peri=2*np.pi*np.arange(9)/(1-3*value**2)
                ax.plot(np.cos(peri)/1.55,np.sin(peri)/1.55,'o',color=BLUE,zorder=5,ms=3)
                theta=0.8;r0=1/(1+0.55*np.cos((1-3*value**2)*theta));tip=(r0*np.cos(theta),r0*np.sin(theta))
                arrow(ax,(0,0),tip,GREEN,mutation_scale=1)
                label(tip,r'$r(\theta)$',GREEN,offset=(8,9))
        elif kind=='light_bending':
            axes((-3.5,3.5),(-1,2),x='',y='');ax.plot(0,0,'o',color=GREY,zorder=5,ms=16)
            ax.plot([-3.2,3.2],[1,1],color=RED,lw=1.4);label((2.2,1.05),'$M=0$',RED)
            q=0.06;t=np.linspace(-0.08,np.pi+0.08,1500);r=1/(np.sin(t)+q*(1+np.cos(t)**2));x=r*np.cos(t);y=r*np.sin(t);ok=abs(x)<3.2
            ax.plot(x[ok],y[ok],color=BLUE,lw=1.4);label((3.2,float(y[ok][np.argmax(x[ok])])),'$M>0$',BLUE,offset=(0,8),ha='right')
            arrow(ax,(-2.3,1),(-1.8,1),RED,mutation_scale=1)
            _ix=np.argsort(x[ok]);_xx=x[ok][_ix];_yy=y[ok][_ix]
            arrow(ax,(-2.3,float(np.interp(-2.3,_xx,_yy))),(-1.9,float(np.interp(-1.9,_xx,_yy))),BLUE,mutation_scale=1)
            ax.plot([0.18,0.18],[0,1],':',color=GREEN,lw=1)
            label((0.18,0.42),'$L/E$',GREEN,offset=(7,0))
            for x,t in [((-2.5,0.2),r'$2ME/L$'),((2.5,0.2),r'$-2ME/L$')]:label(x,t,BLUE,offset=(0,0),ha='center')
        elif kind=='loop':
            ax.set_xlim(-1,4.8);ax.set_ylim(-0.5,3.6)
            p=np.array([0.,0.]);q=np.array([2.6,0.]);r=np.array([3.5,2.]);s=np.array([0.9,2.])
            pts=[p,q,r,s,p]
            for i in range(4):
                arrow(ax,pts[i],pts[i+1],GREY,mutation_scale=1)
                label((pts[i]+pts[i+1])/2,f'$\\gamma_{i+1}$',GREY,offset=[(0,-22),(15,0),(0,12),(-34,12)][i],ha=['center','left','center','right'][i])
            for pt,delta,txt,c in [(p,[0.15,0.8],'$Z_p$',RED),(q,[0.05,0.9],'$Z_1$',RED),(r,[-0.1,0.8],'$Z_2$',RED),(s,[-0.35,0.72],'$Z_3$',RED),(p,[-0.5,0.65],'$Z_4$',BLUE)]:
                tip=pt+delta;arrow(ax,pt,tip,c);label(tip,txt,c,offset=(0,6),ha='center')
            for pt,txt,off in [(p,'$p$',(-12,-14)),(q,r'$\varepsilon X$',(3,-18)),(r,r'$\varepsilon X+\delta Y$',(3,-18)),(s,r'$\delta Y$',(-24,-18))]:label(pt,txt,offset=off)
        else:
            raise ValueError(kind)
        return fig
    return (lecture_sketch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Last time

    Estimators, bias, SE and MSE.

    $X_1,\ldots,X_n\sim f_X$ iid with unknown parameter $\theta$.

    $\hat\theta_n=u(X_1,\ldots,X_n)$ &nbsp; estimator for $\theta$.

    $$
    \begin{aligned}
    \mathrm{Bias}(\hat\theta_n)&=E[\hat\theta_n-\theta]
    &&\text{expected error},\\
    \mathrm{SE}(\hat\theta_n)&=\sqrt{\mathrm{Var}(\hat\theta_n)}
    &&\text{typical error range for unbiased estimators},\\
    \mathrm{MSE}(\hat\theta_n)&=E[(\hat\theta_n-\theta)^2]
    &&\text{square of typical error range for any estimator}\\
    &=\mathrm{Bias}(\hat\theta_n)^2+\mathrm{SE}(\hat\theta_n)^2.
    \end{aligned}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    If $\mathrm{Bias}(\hat\theta_n)\to0$ and $\mathrm{SE}(\hat\theta_n)\to0$ as $n\to\infty$

    $\qquad\Longleftrightarrow\quad$ $\mathrm{MSE}(\hat\theta_n)\to0$ as $n\to\infty$,

    then

    $$
    P(|\hat\theta_n-\theta|\ge\varepsilon)\longrightarrow0
    \quad\text{as }n\to\infty,\quad\forall\,\varepsilon>0.
    $$
    """,'')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $\leadsto$ &nbsp; $\hat\theta_n$ has arbitrarily large probability of being arbitrarily close to $\theta$ for sufficiently large sample size $n$!

    $\leadsto$ &nbsp; $\hat\theta_n$ is a **consistent estimator** for $\theta$ &nbsp; $\leadsto$ &nbsp; a good estimator!

    **In this lecture:** for fixed $n$, how close and with what probability?

    $\leadsto$ &nbsp; confidence intervals for $\theta$.

    ## V.2 &nbsp; Confidence intervals

    **Example.** Midterm scores $X\sim \mathcal{N}(\mu,20^2)$, $\mu$ unknown.

    $\leadsto$ &nbsp; given 4 scores $X_1=30$, $X_2=54$, $X_3=62$, $X_4=78$ &nbsp; $\Longrightarrow$ &nbsp; $M_4=56$.

    How close is $M_4$ to $\mu$? With what probability?

    $$
    M_4=\frac{X_1+X_2+X_3+X_4}{4}
    \sim \mathcal{N}\Bigl(\mu,\frac{20^2}{4}\Bigr).
    $$

    <span class="math-notes"><span>$\displaystyle \frac{20^2}{4}=10^2=\mathrm{SE}(M_4)^2$</span></span>

    $$
    \Longrightarrow\quad Z_4=\frac{M_4-\mu}{\mathrm{SE}(M_4)}\sim \mathcal{N}(0,1)
    \qquad\text{(since }X\text{ is normal)}.
    $$

    $$
    \begin{aligned}
    \Longrightarrow\quad P\bigl(|M_4-\mu|<z\,\mathrm{SE}(M_4)\bigr)
    &=P(|Z_4|<z)\\[1.6em]
    &=\Phi(z)-\Phi(-z)=1-\alpha.
    \end{aligned}
    $$

    <span class="math-notes"><span>$\displaystyle \varepsilon=z\,\mathrm{SE}(M_4)\quad(\text{error threshold})$</span><span>$\displaystyle \Phi(z)-\Phi(-z)\quad(\text{confidence level})$</span></span>

    $\Longrightarrow$ &nbsp; $M_4$ is within $\varepsilon=z\,\mathrm{SE}(M_4)$ of $\mu$ with probability
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    1-\alpha=\Phi(z)-\Phi(-z)=2\Phi(z)-1.
    $$

    $$
    1-\alpha\text{ chance of }
    M_4\in[\mu-\varepsilon,\mu+\varepsilon]
    $$

    <span class="math-notes"><span>$\displaystyle 1-\alpha\quad(\text{found})$</span><span>$\displaystyle [\mu-\varepsilon,\mu+\varepsilon]\quad(\text{given})$</span></span>

    $$
    \Updownarrow
    $$

    $$
    [M_4-\varepsilon,M_4+\varepsilon]
    \ni\mu\text{ with confidence level }1-\alpha.
    $$

    <span class="math-notes"><span>$\displaystyle [M_4-\varepsilon,M_4+\varepsilon]\quad(\text{found})$</span><span>$\displaystyle 1-\alpha\quad(\text{given})$</span></span>

    $$
    \varepsilon=20\quad\Longrightarrow\quad
    1-\alpha=2\Phi(z)-1=2\Phi(2)-1\approx95.4\%.
    $$

    $\Longrightarrow$ &nbsp; $95.4\%$ chance of $M_4\in[\mu-20,\mu+20]$.

    $M_4=56$ … is it close? Doesn't help us locate $\mu$…
    """)
    return


@app.cell(hide_code=True)
def _(lecture_sketch, mo):
    _fig = lecture_sketch('fixed_interval')
    mo.hstack([_fig],justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    1-\alpha=95\%\quad\Longrightarrow\quad
    \varepsilon=\Phi^{-1}(1-\alpha/2)\mathrm{SE}(M_4)
    =10\Phi^{-1}(0.975)\approx19.6.
    $$

    $\Longrightarrow$ &nbsp; $[M_4-19.6,M_4+19.6]\ni\mu$ with $95\%$ confidence.

    $\leadsto$ &nbsp; $M_4=56$ gives $[36.4,75.6]$, a $95\%$ confidence interval for $\mu$.

    $\leadsto$ &nbsp; gives us a range expected to contain $\mu$ at a desired level.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    sample_mean = mo.ui.slider(20,80,step=1,value=56,label=r"$M_4$",show_value=True)
    return (sample_mean,)


@app.cell(hide_code=True)
def _(lecture_sketch, mo, sample_mean):
    _fig = lecture_sketch('moving_interval',sample_mean.value)
    mo.vstack([mo.hstack([sample_mean],justify="start",gap=2,wrap=True),mo.hstack([_fig],justify="center")],gap=1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** For different sample data $X_i=x_i$, we have different sample mean $M_4=m_4$.

    $\Longrightarrow$ &nbsp; different interval $[m_4-\varepsilon,m_4+\varepsilon]$ at the same confidence level $1-\alpha$.
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    Given $X_1,\ldots,X_n\sim f_X$ iid with unknown parameter $\theta$, a **confidence interval** for $\theta$ at level $1-\alpha$ is a pair of statistics

    $$
    L_n=\ell(X_1,\ldots,X_n),\qquad U_n=u(X_1,\ldots,X_n)
    $$

    such that

    $$
    P(L_n\le\theta\le U_n)=1-\alpha.
    $$
    """,'')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example.** $X_1,\ldots,X_4\sim \mathcal{N}(\mu,20^2)$,

    $$
    \Longrightarrow\quad L_4=M_4-z\,\mathrm{SE}(M_4),\qquad
    U_4=M_4+z\mathrm{SE}(M_4),
    $$

    <span class="math-notes"><span>$\displaystyle \mathrm{SE}(M_4)=\sigma/\sqrt n=20/2=10$</span></span>

    where $\Phi(z)=1-\alpha/2$ &nbsp; $\leadsto$ &nbsp; $z=z_{1-\alpha/2}$.

    **Remark.** For $X_1,\ldots,X_n\sim \mathcal{N}(\mu,\sigma^2)$ iid, with known $\sigma^2>0$, we can find the error threshold $\varepsilon=z_{1-\alpha/2}\mathrm{SE}(M_n)$ since

    $$
    Z_n=\frac{M_n-\mu}{\sigma/\sqrt n}
    =\frac{M_n-\mu}{\mathrm{SE}(M_n)}\sim \mathcal{N}(0,1).
    $$

    In general, for nonnormal $X$ with finite positive variance, we need the CLT!

    $$
    Z_n\xrightarrow{d}Z\sim \mathcal{N}(0,1)\qquad\text{as }n\to\infty.
    $$

    **Remark.** $\varepsilon=z\,\mathrm{SE}(M_n)=z\sigma/\sqrt n$ depends explicitly on $\sigma$.

    If $\sigma$ is unknown, we cannot get $\varepsilon$ from

    $$
    P\left(\left|\frac{M_n-\mu}{\sigma/\sqrt n}\right|<z\right)=1-\alpha
    \qquad\text{(even for }X\sim \mathcal{N}(\mu,\sigma^2)\text{)}.
    $$

    In this case, we must use $S_n^2$ (consistent for $\sigma^2$) instead of $\sigma^2$!
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    For iid samples from any population $X$ with $E[X]=\mu$, $0<\mathrm{Var}(X)=\sigma^2<\infty$, both unknown, for large $n$,

    $$
    \left[M_n-z_{1-\alpha/2}\frac{S_n}{\sqrt n},\ M_n+z_{1-\alpha/2}\frac{S_n}{\sqrt n}\right]
    $$

    is an approximate confidence interval for $\mu$ at level $1-\alpha$:

    $$
    P\left(M_n-z_{1-\alpha/2}\frac{S_n}{\sqrt n}\le\mu\le
    M_n+z_{1-\alpha/2}\frac{S_n}{\sqrt n}\right)\longrightarrow1-\alpha
    \quad\text{as }n\to\infty.
    $$
    """,'')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Example (poll).**

    $$
    X=\begin{cases}1&\text{if supports A},\\0&\text{otherwise}.
    \end{cases}
    $$

    $$
    X_1,\ldots,X_n\sim\mathrm{Binom}(1,p)\text{ iid},\qquad
    \mu=p,\quad\sigma^2=p(1-p)
    $$

    <span class="math-notes"><span>$\displaystyle p\quad(\text{fraction of all voters who support A})$</span></span>

    both unknown.

    $$
    \hat p=M_n=\text{fraction of polled voters who support A}.
    $$

    $$
    \hat p(1-\hat p)=\hat\sigma_n^2=\text{biased sample variance}
    =\frac{n-1}{n}S_n^2.
    $$

    $$
    \Longrightarrow\quad
    \left[\hat p-z_{1-\alpha/2}\sqrt{\frac{\hat p(1-\hat p)}{n-1}},\
    \hat p+z_{1-\alpha/2}\sqrt{\frac{\hat p(1-\hat p)}{n-1}}\right]
    $$

    is a confidence interval for $p$ at level $\approx1-\alpha$.

    $n=1000$, with $540$ supporters:

    $$
    \Longrightarrow\quad\hat p=0.54,\qquad
    \sqrt{\frac{\hat p(1-\hat p)}{n-1}}\approx0.0158.
    $$

    $$
    \begin{aligned}
    1-\alpha=95\%&\quad\Longrightarrow\quad z_{1-\alpha/2}\approx1.96
    \quad\Longrightarrow\quad\varepsilon\approx1.96\times0.0158\approx0.031,\\
    1-\alpha=99\%&\quad\Longrightarrow\quad z_{1-\alpha/2}\approx2.576
    \quad\Longrightarrow\quad\varepsilon\approx2.576\times0.0158\approx0.04.
    \end{aligned}
    $$

    $\Longrightarrow$ &nbsp; $[0.54-0.031,0.54+0.031]$ for $p$ at approximate level $0.95$,

    $[0.54-0.04,0.54+0.04]$ at approximate level $0.99$.

    $\leadsto$ &nbsp; we estimate $p$ to be $54\%$, with margin of error $\pm3.1$ percentage points at $95\%$ confidence ($\pm4$ at $99\%$).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At the same $n$: more confidence $\Longleftrightarrow$ larger margin of error.

    $z_{1-\alpha/2}$ grows with $1-\alpha$.

    **Example.** How many voters are needed for given margin $\varepsilon$ and confidence level $1-\alpha$?

    $\hat p=$ fraction of polled voters in support of A.

    $$
    \Longrightarrow\quad\operatorname{Im}(\hat p)=S_{\hat p}
    =\{0,1/n,\ldots,1\}\subset[0,1]
    $$

    $$
    \Longrightarrow\quad\hat p(1-\hat p)\in[0,1/4]
    $$

    <span class="math-notes"><span>$\displaystyle 1/4\quad(\text{worst case})$</span></span>

    $$
    \Longrightarrow\quad z_{1-\alpha/2}\sqrt{\frac{\hat p(1-\hat p)}{n-1}}
    \le z_{1-\alpha/2}\frac1{2\sqrt{n-1}}\le\varepsilon
    $$

    $$
    \Longleftrightarrow\quad n-1\ge\left(\frac{z_{1-\alpha/2}}{2\varepsilon}\right)^2.
    $$

    $\therefore$ &nbsp; to reduce the margin by a factor $1/2$ at the same confidence level, we need about $4$ times as many polled voters!

    **Remark.** We mainly considered $M_n$, which

    1. is unbiased,
    2. has simple standard error,
    3. satisfies the CLT!

    For other statistics $\hat\theta_n$, we need

     a) some asymptotic behavior as $n\to\infty$,

     b) some knowledge about bias and standard error.
    """)
    return


@app.cell(hide_code=True)
def _(definition):
    definition(r"""
    $\hat\theta_n$ is called **asymptotically normal** if, $\forall\,z\in\mathbb R$,

    $$
    P\Bigg(\frac{\hat\theta_n-E[\hat\theta_n]}{\mathrm{SE}(\hat\theta_n)}<z\Bigg)
    \longrightarrow\Phi(z)\quad\text{as }n\to\infty.
    $$

    <span class="math-notes"><span>$\displaystyle \frac{\hat\theta_n-E[\hat\theta_n]}{\mathrm{SE}(\hat\theta_n)}\quad(\text{standard score of }\hat\theta_n)$</span></span>
    """,'')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Or another distribution, with its corresponding CDF.

    $\leadsto$ &nbsp; other asymptotic behaviors give rise to different relations between margins of error $\varepsilon=z\,\mathrm{SE}(\hat\theta_n)$ and confidence levels (in the normal case, $1-\alpha=\Phi(z)-\Phi(-z)$).
    """)
    return


@app.cell(hide_code=True)
def _(theorem):
    theorem(r"""
    If $\hat\theta_n$ is asymptotically normal and the standard error and bias are known,

    $$
    \mathrm{SE}(\hat\theta_n)=A_n,\qquad\mathrm{Bias}(\hat\theta_n)=B_n,
    $$

    then

    $$
    [\hat\theta_n-B_n-z_{1-\alpha/2}A_n,\ \hat\theta_n-B_n+z_{1-\alpha/2}A_n]
    $$

    is an approximate CI for $\theta$ at level $1-\alpha$ for large $n$.
    """,'')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Remark.** If $\mathrm{SE}(\hat\theta_n)$ and $\mathrm{Bias}(\hat\theta_n)$ are unknown, we must find appropriate estimators for $A_n$ and $B_n$.

    $\leadsto$ &nbsp; these are not guaranteed to exist!
    """)
    return


if __name__ == "__main__":
    app.run()
