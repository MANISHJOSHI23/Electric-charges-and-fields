# example.py

from manim import *  # or: from manimlib import *

from manim_slides import Slide


def ir(a,b): # inclusive range, useful for TransformByGlyphMap
    return list(range(a,b+1))


class LatexItems(Tex):
    def __init__(self, *args, page_width="15em", itemize="itemize", **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{itemize}}}YourTextHere\end{{{itemize}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args, tex_template=template, tex_environment=None, **kwargs)


class TransformByGlyphMap(AnimationGroup):
    def __init__(self, mobA, mobB, *glyph_map, replace=True, from_copy=True, show_indices=False, **kwargs):
		# replace=False does not work properly
        if from_copy:
            self.mobA = mobA.copy()
            self.replace = True
        else:
            self.mobA = mobA
            self.replace = replace
        self.mobB = mobB
        self.glyph_map = glyph_map
        self.show_indices = show_indices

        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []
        for from_indices, to_indices in self.glyph_map:
            print(from_indices, to_indices)
            if len(from_indices) == 0 and len(to_indices) == 0:
                self.show_indices = True
                continue
            elif len(to_indices) == 0:
                animations.append(FadeOut(
                    VGroup(*[self.mobA[0][i] for i in from_indices]),
                    shift = self.mobB.get_center()-self.mobA.get_center()
                ))
            elif len(from_indices) == 0:
                animations.append(FadeIn(
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    shift = self.mobB.get_center() - self.mobA.get_center()
                ))
            else:
                animations.append(Transform(
                    VGroup(*[self.mobA[0][i].copy() if i in mentioned_from_indices else self.mobA[0][i] for i in from_indices]),
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    replace_mobject_with_target_in_scene=self.replace
                ))
            mentioned_from_indices.extend(from_indices)
            mentioned_to_indices.extend(to_indices)

        print(mentioned_from_indices, mentioned_to_indices)
        remaining_from_indices = list(set(range(len(self.mobA[0]))) - set(mentioned_from_indices))
        remaining_from_indices.sort()
        remaining_to_indices = list(set(range(len(self.mobB[0]))) - set(mentioned_to_indices))
        remaining_to_indices.sort()
        print(remaining_from_indices, remaining_to_indices)
        if len(remaining_from_indices) == len(remaining_to_indices) and not self.show_indices:
            for from_index, to_index in zip(remaining_from_indices, remaining_to_indices):
                animations.append(Transform(
                    self.mobA[0][from_index],
                    self.mobB[0][to_index],
                    replace_mobject_with_target_in_scene=self.replace
                ))
            super().__init__(*animations, **kwargs)
        else:
            print(f"From indices: {len(remaining_from_indices)}    To indices: {len(remaining_to_indices)}")
            print("Showing indices...")
            super().__init__(
                Create(index_labels(self.mobA[0], color=PINK)),
                FadeIn(self.mobB.next_to(self.mobA, DOWN), shift=DOWN),
                Create(index_labels(self.mobB[0], color=PINK)),
                Wait(5),
                lag_ratio=0.5
                )


class Obj(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.play(Write(title))
        #self.play(Rotate(title,2*PI))
        self.next_slide()
        Outline = Tex('Learning Objectives :',color=BLUE)
        self.play(Write(Outline))
        self.next_slide()
        self.play(Outline.animate.next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8))
        self.next_slide()
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        self.play(Write(list[0]))
        self.next_slide()
        self.play(Write(list[1]))
        self.next_slide()
        self.play(Write(list[2]))
        self.next_slide()
        self.play(Write(list[3]))
        self.next_slide()
        self.play(Write(list[4]))
        self.next_slide()
        self.play(Write(list[5]))
        self.next_slide()
        self.play(Write(list[6]))
        self.next_slide()
        self.play(Write(list[7]))
        self.next_slide()
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(Write(list2[0]))
        self.next_slide()
        self.play(Write(list2[1]))
        self.next_slide()
        self.play(Write(list2[2]))
        self.next_slide()
        self.play(Write(list2[3]))
        self.next_slide()
        self.play(Write(list2[4]))
        self.next_slide()
        self.play(Write(list2[5]))
        self.next_slide()
        self.play(Write(list2[6]))
        self.next_slide()
        self.play(Write(list2[7]))
        self.next_slide(loop=True)
        self.play(FocusOn(list[0]))
        self.play(Circumscribe(list[0]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Introduction', color=BLUE)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()


class Intro(Slide):
    def construct(self):
        Intro_title = Title('Introduction', color=BLUE)
        self.add(Intro_title)
        Obser = Tex('Daily Observations :',color=BLUE).next_to(Intro_title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(Write(Obser))
        self.next_slide()
        list = BulletedList('All of us have the experience of seeing a spark or hearing a crackle when we take off our synthetic clothes or sweater, particularly in dry weather.',
                             'Another common example of electric discharge is the lightning that we see in the sky during thunderstorms.',
                             'We also experience a sensation of an electric shock either while opening the door of a car or holding the iron bar of a bus after sliding from our seat.',
                              'This is due to generation of static electricity', 'Static means anything that does not move or change with time',
                              'Electrostatics deals with the study of forces, fields and potentials arising from static charges.' ).scale(0.7).next_to(Obser,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        self.play(Write(list[0]))
        img1 = ImageMobject('img_1.jpg').next_to(list[0],DOWN).to_corner(RIGHT).scale(0.8)
        self.play(FadeIn(img1))
        self.next_slide()
        self.play(FadeOut(img1))
        self.play(Write(list[1]))
        img2 = ImageMobject('img_2.jpg').next_to(list[0],DOWN, buff=0.5).to_corner(RIGHT).scale(0.8)
        self.play(FadeIn(img2))
        self.next_slide()
        self.play(FadeOut(img2))
        self.play(Write(list[2]))
        img3 = ImageMobject('img_3.jpg').next_to(list[0],DOWN,buff=1).to_corner(RIGHT).scale(0.45)
        self.play(FadeIn(img3))
        self.next_slide()
        self.play(FadeOut(img3))
        self.play(Write(list[3]))
        self.next_slide()
        self.play(Write(list[4]))
        self.next_slide()
        self.play(Write(list[5]))
        self.next_slide()
        

class Charge(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list[1]))
        self.play(Circumscribe(list[1]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Charge_title = Title('Electric Charges and Their Properties ', color=GREEN)
        self.play(ReplacementTransform(title,Charge_title))
        list3 = BulletedList('All matter is made of Atoms.').scale(0.7).next_to(Charge_title,DOWN).to_edge(LEFT).shift(0.5*RIGHT)
        self.play(Write(list3[0]))
        orbit1 = Circle(1,color=YELLOW).shift(3*LEFT)
        orbit2 = Circle(2,color=YELLOW).shift(3*LEFT)
        Atom_txt = Tex('Atom',color=PINK).scale(0.6).next_to(orbit2,DOWN)
        self.play(Create(orbit1),Create(orbit2),Write(Atom_txt))
        point1 =Circle(radius=0.05,color=ORANGE).set_fill(ORANGE, opacity=0.6).shift(3*LEFT)
        point2 =Circle(radius=0.05,color=GREY).set_fill(GREY, opacity=0.6).shift(3*LEFT)
        point3 =Circle(radius=0.05,color=BLUE).set_fill(BLUE, opacity=0.6)
        g1=VGroup(point1.copy().next_to(point1,LEFT,buff=0),point1.copy().next_to(point1,RIGHT,buff=0),point1.copy().next_to(point1,UP,buff=0),point1.copy().next_to(point1,DOWN,buff=0),point2.copy().next_to(point1,UL,buff=0),point2.copy().next_to(point1,DR,buff=0),point2.copy().next_to(point1,UR,buff=0),point2.copy().next_to(point1,DL,buff=0),point2)
        self.play(Create(g1))
        self.play(Create(VGroup(point3.next_to(orbit1,RIGHT,buff=-0.05),point3.copy().next_to(orbit1,LEFT,buff=-0.05),point3.copy().next_to(orbit2,UP,buff=-0.05),point3.copy().next_to(orbit2,DOWN,buff=-0.05))))
        self.next_slide()
        nu=g1.copy()
        self.play(nu.animate.next_to(orbit2,UR).shift(1.5*RIGHT).scale(2))
        nu_txt = Tex('Nucleus',color=RED_C).next_to(nu,DOWN).scale(0.6)
        self.play(Write(nu_txt))
        proton = nu.submobjects[0].copy()
        self.next_slide()
        self.play(proton.animate.next_to(nu, DOWN,buff=1.75))
        self.play(Create(Arrow(nu_txt,proton)))
        proton_txt = Tex('Proton',color=GREEN_D).next_to(nu,DOWN,buff=2).scale(0.6)
        self.play(Write(proton_txt))
        self.next_slide()
        neutron = nu.submobjects[5].copy()
        self.play(neutron.animate.next_to(nu, DOWN,buff=1.75).shift(2.5*RIGHT))
        self.play(Create(Arrow(nu_txt,neutron,max_tip_length_to_length_ratio=0.15)))
        neutron_txt = Tex('Neutron',color=GREEN_D).next_to(nu,DOWN,buff=2).scale(0.6).shift(2.5*RIGHT)
        self.play(Write(neutron_txt))
        self.next_slide()
        electron = point3.copy()
        self.play(electron.animate.next_to(nu, DOWN,buff=1.75).scale(2).shift(5*RIGHT))
        electron_txt = Tex('Electron',color=GREEN_D).next_to(nu,DOWN,buff=2).scale(0.6).shift(5*RIGHT)
        self.play(Write(electron_txt))
        self.next_slide()
        mass_label = MathTex('Mass\ : ').scale(0.4).next_to(proton_txt,DOWN).shift(1.5*LEFT+0.05*DOWN)
        mp = MathTex(r"M_p = 1.67 \times 10^{-27}\ kg ").scale(0.4).next_to(proton_txt, DOWN)
        mn = MathTex(r"M_n = 1.68 \times 10^{-27}\ kg ").scale(0.4).next_to(neutron_txt, DOWN)
        me = MathTex(r"M_e = 9.11 \times 10^{-31}\ kg ").scale(0.4).next_to(electron_txt, DOWN)
        self.play(Write(mass_label),Write(mp))
        self.next_slide()
        self.play(Write(mn))
        self.next_slide()
        self.play(Write(me))   

        charge_label = MathTex('Charge\ : ').scale(0.4).next_to(mass_label,DOWN).shift(0.1*DOWN)
        qp = MathTex(r"q_p = 1.602 \times 10^{-19}\ C ").scale(0.4).next_to(mp, DOWN)
        qn = MathTex(r"q_n = 0 \ C\ (Neutral) ").scale(0.4).next_to(mn, DOWN)
        qe = MathTex(r"q_e = -1.602 \times 10^{-19}\ C ").scale(0.4).next_to(me, DOWN)
        self.next_slide()
        self.play(Write(charge_label),Write(qp))
        self.next_slide()
        self.play(Write(qn))
        self.next_slide()
        self.play(Write(qe))   
        self.wait()

class Charge2(Slide):
    def construct(self):
        Charge_title = Title('Electric Charges and Their Properties', color=GREEN)
        self.add(Charge_title)
        list = BulletedList('Charge is a fundamental property of matter by virtue of which it produces and experience electromagnetic force.','Electromagnetic forces can be attractive or repulsive. In contrast with the gravitational froce between masses which is always attractive. ', "There are two kinds of electric charges which are distinguished form each other by calling one kind as 'posiitve' and the other as 'negative', these names are arbitraily chosen by Benjamin Franklin. ",'Like chagres repel each other and Unlike charges attract each other', ).scale(0.7).next_to(Charge_title,2*DOWN).to_corner(LEFT).shift(RIGHT)
        list2=BulletedList('Charge is a scalar quantitiy.','S.I unit of charge is coulomb (C)', 'C.G.S. unit of charge is esu (electrostatic unit) or static coloumb (stat C or franklin)','1 C $= 3\\times 10^{9}$ stat C','Dimension formula of charge [Q]=[AT]   $(\\because Q=It)$','A charge cannot exist without masss (however a mass can exist without charge e.g. neutron) ').scale(0.7).next_to(Charge_title,2*DOWN).to_corner(LEFT).shift(RIGHT)
        chq_trn_lbl = Tex('Charge is transferable :',color=BLUE).next_to(Charge_title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        list3 =BulletedList('Charge can be transfered from one body to another.','Neutral Body $+$ electron $\\rightarrow$ Negatively charge body','Neutral Body $-$ electron $\\rightarrow$ Positively charge body','When we charge an object, the mass of the body changes because wherever there is charge, there is mass.').scale(0.7).next_to(chq_trn_lbl,DOWN).to_corner(LEFT).shift(RIGHT)
        frc_elc_lbl = Tex('Frictional Electricity :',color=BLUE).next_to(list3,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        list4 =BulletedList('When two bodies are rubbed together under friction electrons are transferred from one body to the other. As a result one body becomes positively charged while the other gets negatively charged.').scale(0.7).next_to(frc_elc_lbl,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(list[0]))
        self.next_slide()
        self.play(Write(list[1]))
        self.next_slide()
        self.play(Write(list[2]))
        self.next_slide()
        self.play(Write(list[3]))
        self.next_slide()
        self.play(FadeOut(list))
        self.play(Write(list2[0]))
        self.next_slide()
        self.play(Write(list2[1]))
        self.next_slide()
        self.play(Write(list2[2]))
        self.next_slide()
        self.play(Write(list2[3]))
        self.next_slide()
        self.play(Write(list2[4]))
        self.next_slide()
        self.play(Write(list2[5]))
        self.next_slide()
        self.play(FadeOut(list2))
        self.play(Write(chq_trn_lbl))
        self.next_slide()
        self.play(Write(list3[0]))
        self.next_slide()
        self.play(Write(list3[1]))
        self.next_slide()
        self.play(Write(list3[2]))
        self.next_slide()
        self.play(Write(list3[3]))
        self.next_slide()
        self.play(Write(frc_elc_lbl))
        self.next_slide()
        self.play(Write(list4[0]))
        self.next_slide()
        self.play(FadeOut(list3,frc_elc_lbl,list4,chq_trn_lbl))
        self.next_slide()
        add_lbl = Tex('Additivity of Charges :',color=BLUE).next_to(Charge_title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(Write(add_lbl))
        list5 =BulletedList(' If a system contains n charges $q_1,\ q_2,\ q_3,\ ..., q_n$ , then the total charge of the system is $q_1 + q_2 + q_3 + ... + q_n$ . i.e., charges add up like real numbers or they are scalars',' Proper signs have to be used while adding the charges in a system.','Example:  Total charge $(Q)=q_1+q_2+q_3+q_4$','$(Q)=5\ C+(-2\ C)+3\ C+(-7\ C)=-1\ C$').scale(0.7).next_to(chq_trn_lbl,DOWN).to_corner(LEFT).shift(RIGHT)
        self.next_slide()
        self.play(Write(list5[0]))
        self.next_slide()
        self.play(Write(list5[1]))
        cir = Circle(1.5).next_to(list5[1],DOWN).to_edge(RIGHT).shift(LEFT)
        q1=Dot(cir.get_center(),color=YELLOW).shift(0.9*LEFT)
        q1_text=Tex('$q_1=5 C$').next_to(q1,DOWN,buff=0).scale(0.5)
        q2=Dot(cir.get_center(),color=ORANGE).shift(0.9*RIGHT)
        q2_text=Tex('$q_2=-2 C$').next_to(q2,DOWN,buff=0).scale(0.5)
        q3=Dot(cir.get_center(),color=PURPLE_A).shift(0.5*DOWN)
        q3_text=Tex('$q_3=3 C$').next_to(q3,DOWN,buff=0).scale(0.5)
        q4=Dot(cir.get_center(),color=GREEN_D).shift(0.8*UP)
        q4_text=Tex('$q_4=-7 C$').next_to(q4,DOWN,buff=0).scale(0.5)
        self.play(Create(cir),Create(VGroup(q1,q2,q3,q4)),Write(VGroup(q1_text,q2_text,q3_text,q4_text)))
        self.next_slide()
        self.play(Write(list5[2]))
        self.next_slide()
        self.play(Write(list5[3]))
        self.next_slide()


class Charge3(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")
        Charge_title = Title('Electric Charges and Their Properties', color=GREEN)
        self.add(Charge_title)
        cons_lbl = Tex('Conservation of Charges :',color=BLUE).next_to(Charge_title,DOWN).to_corner(LEFT).scale(0.8)
        self.play(Write(cons_lbl))
        list =BulletedList('Charge can neither be created nor destroyed; it can only be transferred from place to place, from one object to another.', 'Within an isolated system consisting of many charged bodies, due to interactions among the bodies, charges may get redistributed but it is found that the total charge of the isolated system is always conserved.',' Sometimes nature creates charged particles from an uncharged particle: a neutron turns into a proton and an electron.','Neutron $(q_n =0)$ $\\Rightarrow$ Proton $(q_p=+e)$ $+$ Electron $(q_e=-e)$ ','Pair Production:', 'Gamma Ray photon $(q_\gamma =0)$ $\\Rightarrow$ Positron $(q_{e^{+}}=+e)$ $+$ Electron $(q_e=-e)$').scale(0.7).next_to(cons_lbl,DOWN).to_corner(LEFT).shift(RIGHT)
        self.next_slide()
        self.play(Write(list[0]))
        self.next_slide()
        self.play(Write(list[1]))
        self.next_slide()
        self.play(Write(list[2]))
        self.next_slide()
        self.play(Write(list[3]))
        self.next_slide()
        self.play(Write(list[4]))
        self.next_slide()
        self.play(Write(list[5]))
        self.next_slide()
        self.play(FadeOut(list,cons_lbl))
        self.next_slide()
        quant_lbl = Tex('Quantisation of charge: ',color=BLUE).next_to(Charge_title,DOWN).to_corner(LEFT).scale(0.8)
        self.play(Write(quant_lbl))
        list2 =BulletedList('Quantisation of charge means that electric charge comes in discrete amounts, and there is a smallest possible amount of charge ( $e = 1.602 \\times 10^{-19}$ C ) that an object can have. No free particle can have less charge than this, and, therefore, the charge $(q)$ on any object must be an integer multiple of this amount $(e)$. ').scale(0.7).next_to(cons_lbl,DOWN).to_corner(LEFT).shift(RIGHT)
        form = Tex('$q = ne$   (Where $n=\\pm 1,\ \\pm 2,\ \\pm 3,\ .....$)').next_to(list2,DOWN).scale(0.8)
        self.next_slide()
        self.play(Write(list2[0]))
        self.next_slide()
        self.play(Write(form))
        self.next_slide()
        self.play(Write(BulletedList('For macroscopic charges for which n is a very large number, quantisation of charge can be ignored and charge appears to be continuous.}').next_to(form,DOWN).scale(0.7)))

class Ex1(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 1: If a body has positive charge on it, then it means it has}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) Gained some proton').scale(0.7),Tex('(b) Lost some protons').scale(0.7),Tex('(c) Gained some electrons').scale(0.7),Tex('(d) Lost some electrons').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[3]))

class Ex2(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 2: Which of the following is not true about electric charge }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('\justifying {(a) Charge on a body is always integral muliple of certain charge known as charge of electron}',tex_template=myBaseTemplate).scale(0.7),Tex('\justifying {(b) Charge is a scalar quantity}',tex_template=myBaseTemplate).scale(0.7),Tex('\justifying {(c) Net charge of an isolated system is always conservesd}',tex_template=myBaseTemplate).scale(0.7),Tex('\justifying {(d) Charge can be converted into energy and energy can be converted into charge}',tex_template=myBaseTemplate).scale(0.7) ).arrange_in_grid(4,1,col_alignments='l').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[3]))

class Ex3(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 3: Consider three point objects $P,\ Q$ and $R$. $P$ and $Q$ repel each other, while $P$ and $R$ attract. What is the nature of force between $Q$ and $R$? }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) Repulsive force').scale(0.7),Tex('(b) Attractive force ').scale(0.7),Tex('(c) No force').scale(0.7),Tex('(d) None of these').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[1]))

class Ex4(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 4: When $10^{14}$ electrons are removed from a neutral metal sphere, the charge on the sphere becomes:}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) $16\ \mu$ C').scale(0.7),Tex('(b) $-16\ \mu$ C').scale(0.7),Tex('(c) $32\ \mu$ C').scale(0.7),Tex('(d) $-32\ \mu$ C').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        sol_label =Tex('Solution :', color=ORANGE).next_to(op,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList('Given: No. of electron removed $n = 10^{14}$', 'Find: Charge on the sphere $q = ?$','Using $q= ne$','$q=10^{14}\\times 1.6 \\times 10^{-19}$ C  $=1.6\\times 10^{-5}$ C ','$q=16\\times 10^{-6}$ C $=16\ \mu$ C',dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(sol_label))
        self.next_slide()
        self.play(Write(sol[0]))
        self.next_slide()
        self.play(Write(sol[1]))
        self.next_slide()
        self.play(Write(sol[2]))
        self.next_slide()
        self.play(Write(sol[3]))
        self.next_slide()
        self.play(Write(sol[4]))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[0]))


class Ex5(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 5: A conductor has $14.4\\times 10^{-19}$ C positive charge. The conductor has }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) 9 electron in excess').scale(0.7),Tex('(b) 27 electrons in short').scale(0.7),Tex('(c) 27 electrons in excess').scale(0.7),Tex('(d) 9 electrons in short').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        sol_label =Tex('Solution :', color=ORANGE).next_to(op,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList('Given: Charge on conductor $q = 14.4\\times 10^{-19}$ C', 'Find: No. of electrons short or excess $n = ?$','Using $q= ne$  Or $n =\dfrac{q}{e}$','$n=\dfrac{14.4\\times 10^{-19}\ C}{1.6\\times 10^{-19}\ C} = \dfrac{14.4}{1.6}$','$n=9$',dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(sol_label))
        self.next_slide()
        self.play(Write(sol[0]))
        self.next_slide()
        self.play(Write(sol[1]))
        self.next_slide()
        self.play(Write(sol[2]))
        self.next_slide()
        self.play(Write(sol[3]))
        self.next_slide()
        self.play(Write(sol[4]))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[3]))

class Ex6(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 6:  If $10^9$ electrons move out of a body to another body every second, how much time is required to get a total charge of 1 C on the other body?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList('Given: Number of elctrons moved out in 1 s $= 10^9$ ', '$\\therefore$ Charge moved out in 1 s $=ne = 10^9\\times 1.6 \\times 10^{-19} = 1.6\\times 10^{-10}$  C' ,'Time required to get a charge of $1.6 \\times 10^{-10}$ C $= 1$ s','So, time required to get a charge of 1 C $= \\dfrac{1}{1.6\\times 10^{-10}}$ s $= 6.25\\times 10^{9}$ s','Converting this time in s to years we get $t = \dfrac{6.25\\times 10^9}{365\\times 24 \\times 3600} =198.186$ years',dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(sol_label))
        self.next_slide()
        self.play(Write(sol[0]))
        self.next_slide()
        self.play(Write(sol[1]))
        self.next_slide()
        self.play(Write(sol[2]))
        self.next_slide()
        self.play(Write(sol[3]))
        self.next_slide()
        self.play(Write(sol[4]))

class Ex7(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 7: How much positive and negative charge is there in a cup of water (250 g)?. Given molecular mass of water is 18 g.}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList('Given: Mass of a cup of water $M = 250$ g ', 'Molar mass of water $m = 18$ g' ,'Number of water molecules in 1 cup of water$\\\\= \\dfrac{M}{m}\\times N_A = \\dfrac{250}{18}\\times 6.02 \\times 10^{23} =83.64 \\times 10^{23}$','Number of electron or protons in 1 molecule of water = 10','$\\therefore $ Number of electrons or protons in 1 cup of water  $\\\\n=83.64\\times 10^{23}\\times 10 = 83.64\\times 10^{24}$','Now, Amount of positive or negative charge in 1 cup of water $\\\\ q= ne = 83.64\\times 10^{24}\\times 1.6 \\times 10^{-19}$ C  $=133.8 \\times 10^{5}$ C',dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(sol_label))
        self.next_slide()
        self.play(Write(sol[0]))
        self.next_slide()
        self.play(Write(sol[1]))
        self.next_slide()
        self.play(Write(sol[2]))
        self.next_slide()
        self.play(Write(sol[3]))
        self.next_slide()
        self.play(Write(sol[4]))
        self.next_slide()
        self.play(Write(sol[5]))

class Ex8(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 8: A polythene piece rubbed with wool is found to have a negative charge of $3 \\times 10^{-7}$ C.\\\\ (a) Estimate the number of electrons transferred (from which to which?)\\\\ (b) Is there a transfer of mass from wool to polythene?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        self.play(Write(Tex('Do it yourself !').next_to(sol_label,DOWN).to_edge(LEFT).shift(RIGHT).scale(0.7)))
        self.next_slide()


class Cond(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list[3]))
        self.play(Circumscribe(list[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Cond_title = Title('Conductors and Insulators', color=GREEN)
        self.play(ReplacementTransform(title,Cond_title))
        self.next_slide()
        conductors_lbl = Tex('Conductors :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(Write(conductors_lbl))
        list3 = BulletedList('Those substances which allow electricity to pass through them easily are called conductors.','In conductors outermost electron are loosely bound to the atoms nucleus that are comparatively free to move inside the material.','Examples: Metals, humans and earth','When some charge is transferred to a conductor, it readily gets distributed over the entire surface of the conductor. ').scale(0.7).next_to(conductors_lbl,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        self.next_slide()
        self.play(Write(list3[0]))
        self.next_slide()
        self.play(Write(list3[1]))
        self.next_slide()
        self.play(Write(list3[2]))
        self.next_slide()
        self.play(Write(list3[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list3))
        Insul_lbl = Tex('Insulators :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(ReplacementTransform(conductors_lbl,Insul_lbl))
        self.next_slide()
        list4 = BulletedList('Insulators, in contrast, are made from materials that have bounded electrons(they are not free and it is hard to dislodge these elctrons from the atoms)' ,'In insulators charge flows only with great difficulty, if at all.','If some charge is put on an insulator, it stays at the same place.','Examples: Most of the non-metals like glass, porcelain, plastic, nylon, wood offer high resistance to the passage of electricity through them.').scale(0.7).next_to(Insul_lbl,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        self.next_slide()
        self.play(Write(list4[0]))
        self.next_slide()
        self.play(Write(list4[1]))
        self.next_slide()
        self.play(Write(list4[2]))
        self.next_slide()
        self.play(Write(list4[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list4))
        Eart_lbl = Tex('Earthing Or Grounding :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(ReplacementTransform(Insul_lbl,Eart_lbl))
        self.next_slide()
        list5 = BulletedList('When we bring a charged body in contact with the earth, all the excess charge on the body disappears by causing a momentary current to pass to the ground through the connecting conductor (such as our body)', 'This process of sharing the charges with the earth is called grounding or earthing. ' ).scale(0.7).next_to(Eart_lbl,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        self.next_slide()
        self.play(Write(list5[0]))
        self.next_slide()
        self.play(Write(list5[1]))


class Induc(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list[4]))
        self.play(Circumscribe(list[4]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Cond_title = Title('Charging by Induction', color=GREEN)
        self.play(ReplacementTransform(title,Cond_title))
        self.next_slide()
        Ind_lbl = Tex('Electrostatic Induction :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        img = ImageMobject('ind.png').scale(0.25)
        self.play(Write(Ind_lbl))
        list3 =  LatexItems( r"\item When an electrically charged object is brought   close to the conductor, the charge on the insulator exerts an electric force on the free electrons of the conductor.", 
                            r"\item Since the rod is positively charged, the free electrons  are attracted, flowing toward the rod to the near side of the conductor",  
                            r"\item Now, the conductor is still overall electrically neutral. However, the conductor now has a charge distribution; the near end now has more negative charge than positive charge,",
                            r"\item The result is the formation of what is called an electric dipole.",
                            itemize="itemize" ,page_width="30em").scale(0.7)
        self.next_slide()
        Group(list3,img).arrange(RIGHT).next_to(Ind_lbl,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(FadeIn(img))
        for item in list3:
            self.play(Write(item))
            self.next_slide()
        self.play(FadeOut(list3,img))
        self.next_slide()
        img2 = ImageMobject('paper.png').scale(0.5)
        list4 =  LatexItems( r"\item Neutral objects can be attracted to any charged object.", 
                            r"\item If you run a plastic comb through your hair, the charged comb can pick up neutral pieces of paper.",  
                            r"\item When a charged comb is brought near a neutral insulator(paper), the distribution of charge in atoms and molecules is shifted slightly.",
                            r"\item Opposite charge is attracted nearer the external charged rod, while like charge is repelled. Since the electrostatic force decreases with distance, the repulsion of like charges is weaker than the attraction of unlike charges, and so there is a net attraction.",
                            itemize="itemize" ,page_width="30em").scale(0.7)
        self.next_slide()
        Group(list4,img2).arrange(RIGHT).next_to(Ind_lbl,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(FadeIn(img2))
        for item in list4:
            self.play(Write(item))
            self.next_slide()
        

        self.play(FadeOut(list4,img2))
        Cond1_title = Tex('Charging by induction (1st Method)',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(ReplacementTransform(Ind_lbl,Cond1_title))
        self.next_slide()
        list5 =  BulletedList( "The process of charging  neutral body by bringing a charged object nearby it without making contact between the two bodies is known as charging by induction ").scale(0.7).next_to(Ind_lbl,DOWN).shift(RIGHT).to_corner(LEFT)
        g1 = Group(ImageMobject('ind1.png'),ImageMobject('ind2.png'),ImageMobject('ind3.png'),ImageMobject('ind4.png')).arrange_in_grid(2,2).next_to(list5,DOWN).scale(0.75)
        self.next_slide()
        self.play(Write(list5))
        for item in g1:
            self.play(FadeIn(item))
            self.next_slide()
        
        self.play(FadeOut(list5,g1))
        Cond2_title = Tex('Charging by induction (2nd Method)',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(ReplacementTransform(Cond1_title,Cond2_title))
        self.next_slide()
        g2 = Group(ImageMobject('in1.png'),ImageMobject('in2.png'),ImageMobject('in3.png'),ImageMobject('in4.png')).arrange_in_grid(2,2).next_to(Cond2_title,DOWN).to_corner(LEFT).scale(0.85)
        self.next_slide()
        for item in g2:
            self.play(FadeIn(item))
            self.next_slide()


class Coulm(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list[5]))
        self.play(Circumscribe(list[5]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Coulm_title = Title("Coulomb's Law", color=GREEN)
        self.play(ReplacementTransform(title,Coulm_title))
        self.next_slide()
        q1=Dot(color=YELLOW).shift(0.9*LEFT)
        q1_text=Tex('$q_1$').next_to(q1,DOWN,buff=0).scale(0.5)
        q2=Dot(color=ORANGE).shift(1.5*RIGHT)
        q2_text=Tex('$q_2$').next_to(q2,DOWN,buff=0).scale(0.5)
        arrow = DoubleArrow(q1.get_center(),q2.get_center(), tip_length=0.2, color=YELLOW,buff=0).shift(0.7*DOWN)
        arrow_text=Tex('$r$').next_to(arrow,UP,buff=0).scale(0.5)
        f1_arrow = Arrow(start=q1.get_right(),end=q1.get_right()+[0.8,0,0],buff=0,color=GREEN_D) 
        f1_tex=Tex('$F_1$').next_to(f1_arrow,UP,buff=0).scale(0.5)
        f2_arrow = Arrow(start=q2.get_left(),end=q2.get_left()-[0.8,0,0],buff=0,color=ORANGE)
        f2_tex=Tex('$F_2$').next_to(f2_arrow,UP,buff=0).scale(0.5)
        g1 = VGroup(q1,q2,q1_text,q2_text,arrow,arrow_text,f1_arrow, f1_tex,f2_tex,f2_arrow)
        list3 =  LatexItems( r"\item Coulomb's law is a quantitative statement about the force between two point charges.", 
                            r"\item Coulomb measured the force between two point charges and found that it varied inversely as the square of the distance between the charges and was directly proportional to the product of the magnitude of the two charges and acted along the line joining the two charges. ",
                            r"\item Mathematically, magnitude of electrostatic force $(F)$  between two stationary charges $(q_1,\ q_2)$ seperated by a distance $r$ in vacuum is\\ \[F\propto \dfrac{\left|q_1q_2\right|}{r^2} \qquad \text{Or}\qquad F = k\dfrac{\left|q_1q_2\right|}{r^2}\]",
                            itemize="itemize" ,page_width="30em").scale(0.7)
        self.next_slide()
        Group(list3,g1).arrange(RIGHT,buff=0.3).next_to(Coulm_title,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(Create(g1))
        self.next_slide()
        for item in list3:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(list3))       
        list4 =  LatexItems( r"\item  \[F\propto \dfrac{\left|q_1q_2\right|}{r^2} \qquad \text{Or}\qquad F = k\dfrac{\left|q_1q_2\right|}{r^2}\]",
                            r"\item Where, $k$ is a proportionality constant.", 
                            r"\item In S.I. unit $k=\dfrac{1}{4\pi\epsilon_0}=9\times 10^9\ Nm^2C^{-2}$",
                            r"\item Where $\epsilon_0 =8.854 \times 10^{-12}\ C^2N^{-1}m^{-2}$ and is called the permittivity of free space (vacuum)",
                            r"\item If $q_1=q_2=1\ C$ and $r = 1 $ m. Then, $F=9\times 10^9\ N$",
                            r"\item That is, 1 C is the charge that when placed at a distance of 1 m from another charge of the same magnitude in vacuum experiences an electrical force of repulsion of magnitude $9 \times 10^9$ N.",
                            itemize="itemize" ,page_width="30em").scale(0.7)
        Group(list4,g1).arrange(RIGHT,buff=0.3).next_to(Coulm_title,DOWN).shift(RIGHT).to_corner(LEFT)
        for item in list4:
            self.play(Write(item))
            self.next_slide()
        

        self.play(FadeOut(list4,g1)) 
        Per_title = Tex('Absoloute and Relative Permittivity (Dielectric constant) of Medium:',color=BLUE).scale(0.8).next_to(Outline,DOWN).to_edge(LEFT).shift(1.5*UP)
        self.play(ReplacementTransform(Coulm_title,Per_title))
        self.next_slide()
        list5 = BulletedList("If the point charges are  kept in some other medium (say water) then coulomb's law gives \[F=\dfrac{1}{4\pi\epsilon}\dfrac{q_1q_2}{r^2}\]",
                             "Where, $\epsilon$ is absolute permitivity of the medium \[\dfrac{F_{vacuum}}{F_{medium}}=\dfrac{\dfrac{1}{4\pi \epsilon_0}\dfrac{q_1q_2}{r^2}}{\dfrac{1}{4\pi \epsilon}\dfrac{q_1q_2}{r^2}}=\dfrac{\epsilon}{\epsilon_0}= \epsilon_r (or K)\]",
                             "Where, $\epsilon_r$ is called relative permittivity of the medium and also known as Dielectric constant(K) of the medium.").scale(0.7).next_to(Per_title,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        for item in list5:
            self.play(Write(item))
            self.next_slide()
        

class Coulm_Vec(Slide):
    def construct(self):
        Coulm_title = Title("Coulomb's Law in Vector Form", color=GREEN)
        self.play(Write(Coulm_title))
        self.next_slide()
        ax = Axes(x_range=[0,6],y_range=[0, 6],x_length=10,y_length=8)
        q1 = Dot(ax.coords_to_point(2,5),color=RED).scale(2)
        q2 = Dot(ax.coords_to_point(5,5),color=RED).scale(2)
        q1_text=Tex('$q_1$').next_to(q1,UP,buff=0.2).scale(1.5)
        q2_text=Tex('$q_2$').next_to(q2,UP,buff=0.2).scale(1.5)
        vector_1 = Arrow(ax.coords_to_point(0,0),ax.coords_to_point(2,5),buff=0,color=GREEN)
        vector_2 = Arrow(ax.coords_to_point(0,0),ax.coords_to_point(5,5),buff=0,color=BLUE)
        v1_lbl = MathTex('\\vec{r}_1').scale(1.5).move_to(ax.coords_to_point(0.8,3))
        v2_lbl = Tex('$\\vec{r}_{2}$').scale(1.5).move_to(ax.coords_to_point(3.8,3))
        f1_arrow = Arrow(start=q1.get_left(),end=q1.get_left()-[2.5,0,0],buff=0,color=GREEN_D) 
        f2_arrow = Arrow(start=q2.get_right(),end=q2.get_right()+[2.5,0,0],buff=0)
        f1_lbl = Tex('$\\vec{F}_{12}$').scale(1.5).next_to(f1_arrow,UP)
        f2_lbl = Tex('$\\vec{F}_{21}$').scale(1.5).next_to(f2_arrow,UP)
        vector_3 = Arrow(ax.coords_to_point(2,5),ax.coords_to_point(5,5),buff=0,color=YELLOW)
        v3_lbl = MathTex('\\vec{r}_{21 } ').scale(1.5).move_to(ax.coords_to_point(3.5,5.3))
        vector_4 = Arrow(ax.coords_to_point(5,5),ax.coords_to_point(2,5),buff=0,color=RED).shift(UP)
        v4_lbl = MathTex('\\vec{r}_{12 } ').scale(1.5).next_to(vector_4,UP)
        g1 = VGroup(ax,q1,q2,q1_text,q2_text,vector_1,vector_2,v1_lbl,v2_lbl,f1_arrow,f2_arrow,f1_lbl,f2_lbl,vector_3,v3_lbl,vector_4,v4_lbl).scale(0.45).next_to(Coulm_title,DOWN).to_edge(RIGHT)
        list3 =  LatexItems( r"\item $q_1,\ q_2 \rightarrow$ Two point charges",
                            r"\item $\vec{r}_1,\ \vec{r}_2 \rightarrow$ Position vectors of $q_1$ and $q_2$ ",
                            r"\item $\vec{F}_{12}\rightarrow$ Force on $q_1$ due to $q_2$",
                            r"\item $\vec{F}_{21}\rightarrow$ Force on $q_2$ due to $q_1$",
                            r"\item $\vec{r}_{21}= \vec{r}_{2}-\vec{r}_{1}$ (Vector leading from 1 to 2)",
                            r"\item $\vec{r}_{12}= \vec{r}_{1}-\vec{r}_{2}$ (Vector leading from 2 to 1)",
                            r"\item $\vec{r}_{21}=-\vec{r}_{12}$ and $\left|\vec{r}_{21}\right|=\left|\vec{r}_{12}\right|=r$",
                            r"\item To denote the direction from 1 to 2 (or from 2 to 1), we define the unit vectors:  \\$\hat{r}_{21}=\dfrac{\vec{r}_{21}}{\left|\vec{r}_{21}\right|}$ and $\hat{r}_{12}=\dfrac{\vec{r}_{12}}{\left|\vec{r}_{12}\right|}$  ",
                            itemize="itemize" ,page_width="25em").scale(0.7).next_to(Coulm_title,DOWN).to_edge(LEFT)
        self.next_slide()
        Group(list3,g1).arrange(RIGHT,buff=0.15).next_to(Coulm_title,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(FadeIn(q1,q2),Write(q1_text),Write(q2_text))
        self.next_slide()
        self.play(Write(list3[0]))
        self.next_slide()
        self.play(Create(VGroup(ax,vector_1,vector_2,v1_lbl,v2_lbl)))
        self.play(Write(list3[1]))
        self.next_slide()
        self.play(Create(VGroup(f1_arrow)),Write(f1_lbl))
        self.play(Write(list3[2]))
        self.next_slide()
        self.play(Create(VGroup(f2_arrow)),Write(f2_lbl))
        self.play(Write(list3[3]))
        self.next_slide()
        self.play(Create(VGroup(vector_3,v3_lbl)))
        self.play(Write(list3[4]))
        self.next_slide()
        self.play(Create(VGroup(vector_4,v4_lbl)))
        self.play(Write(list3[5]))
        self.next_slide()
        self.play(Write(list3[6]))
        self.next_slide()
        self.play(Write(list3[7]))
        self.next_slide()
        self.play(g1.animate().scale(0.8))
        list4 =  LatexItems( r"\item $\vec{F}_{21}=\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_2}{|r_{21}|^{2}}\ \hat{r}_{21}$",
                            r"\item $\vec{F}_{12}=\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_2}{|r_{12}|^{2}}\ \hat{r}_{12}$",
                            r"\item $\vec{F}_{21}=-\vec{F}_{12}$",
                            itemize="itemize" ,page_width="15em").scale(0.7)
        g2 = Group(g1,list4).arrange(DOWN,buff=0.1).next_to(Coulm_title,DOWN).shift(RIGHT).to_corner(LEFT)
        Group(list3.scale(0.9),g2).arrange(RIGHT,buff=0.15).next_to(Coulm_title,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(Write(list4[0]))
        self.next_slide()
        self.play(Write(list4[1]))
        self.next_slide()
        self.play(Write(list4[2]))

        
class Ex9(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Exercise 1.1: What is the force between two small charged spheres having charges of $2 \\times 10^{-7} $ C and $3 \\times 10^{-7}$ C placed 30 cm apart in air?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList('Given: $q_1 = 2\\times 10^{-7} $ C and $q_2 = 3\\times 10^{-7}$ C '," $r = 30 $ cm $=30\\times 10^{-2}$ m $=3\\times 10^{-1}$ m","Find : $F = ?$",
                           "Using  Coulomb's Law $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$","$F = 9\\times 10^{9} \\times \\dfrac{2\\times 10^{-7} \\times 3\\times 10^{-7}}{\\left(3\\times 10^{-1}\\right)^{2}}= 9\\times 10^{9}\\times \\dfrac{2\\times 10^{-7} \\times 3\\times 10^{-7}}{9\\times 10^{-2}}$","$F = 10^{9} \\times 2\\times 10^{-7}\\times 3\\times 10^{-7}\\times 10^{2}=6\\times 10^{-3} $ N","This force is repulsive, since the spheres have same charges.",dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(sol_label))
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()


class Ex10(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 9: The sum of two point charges is $7 \ \mu$ C. They repel each other with a force with a force of 1 N when kept at 30 cm apart in free space. Calculate the value of each charge.} ',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList("Given F = 1 N  and $q_1 + q_2 = 7\ \mu$ C", "$r = 30\ cm = 3\\times 10^{-1}$ m","Find: $q_1$ and $q_2$",'Let one of the two charges be $x\ \mu$ C.',"$\\therefore$ Other charge will be $(7-x)\ \mu$ C","Using  Coulomb's Law $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList("$1 N = 9\\times 10^{9}\ Nm^{2}C^{-2} \\times \\dfrac{x \\times 10^{-6}\\times (7-x)\\times 10^{-6}\ C^2}{(3\\times 10^{-1}\ m)^2} $",
                            "$1 N = 9\\times 10^{9}\ Nm^{2}C^{-2} \\times \\dfrac{x \\times 10^{-6}\\times (7-x)\\times 10^{-6}\ C^2}{9\\times 10^{-2}\ m^2} $",
                            "$1 = 10^9\\times x(7-x) \\times 10^{-12}\\times 10^{2}=  x(7-x) \\times 10^{-1}$","$10 = -x^2 + 7x $ Or $x^2-7x +10 = 0$","$(x-2)(x-5)=0$",
                            "$ x = 2$ Or $x= 5$","$\\therefore $ Two point charges are $2\ \mu$ C and $5\ \mu$C.",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        line = Line(sol2.get_top(),sol2.get_bottom(),color=GREEN).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.15).next_to(sol_label,DOWN).to_corner(LEFT)
        self.play(Write(sol_label))
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()
            
            


class Ex11(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Exercise 1.2: The electrostatic force on a small sphere of charge $0.4\ \mu$C due to another small sphere of charge $-0.8\ \mu$C in air is 0.2 N. (a) What is the distance between the two spheres? (b) What is the force on the second sphere due to the first?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)

        sol = BulletedList('Given: : $q_1 = 0.4\ \mu$C , $q_2 = -0.8\ \mu$C and $F = 0.2$ N',"Find : (a) Distance between two charged sphere $r = ?$",
                           "Using  Coulomb's Law $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$","$r^2 = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{F}$","$r^2 = 9\\times 10^9 \ Nm^2C^{-2} \\times \\dfrac{0.4\\times 10^{-6}\\times 0.8\\times 10^{-6}\ C^2}{0.2\ N}$",
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList("$r^2 = 9\\times 10^9 \\times 2\\times 0.8\\times 10^{-12}\ m^2$",
                           "$r^2 = 14.4\\times 10^{-3}\ m^2$","$r^2= 144 \\times 10^{-4}$","$r =\sqrt{144 \\times 10^{-2}\ m^2}$","$r=12\\times 10^{-2}\ m$",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        line = Line(sol.get_top(),sol.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.play(Write(sol_label))
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()


class Ex12(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 10: There are two charges $+2 \ \mu$ C and $-3\ \mu$C. The ratio of forces acting on them will be  }',tex_template=myBaseTemplate, color=BLUE_C).to_edge(UL).scale(0.8)
        op = VGroup(Tex('(a) $2:3$').scale(0.7),Tex('(b) $1:1$ ').scale(0.7),Tex('(c) $3:2$').scale(0.7),Tex('(d) $4:9$').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[1]))


class Ex13(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 11: What is the minimum electric force between two charged particles 1 m apart in free space?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList('Given: : $r = 1$ m',"Find : (a) Minimum force between two charged particles","Force will be minimum when the charge on both particle is minimum,",
                           " $i.e., \ q_1 =q_2 =e = 1.6\\times 10^{-19}$ C",
                           "Using  Coulomb's Law $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$","$F = 9\\times 10^9 \\times \\dfrac{1.6\\times 10^{-19} \\times 1.6\\times  10^{-19}}{1^2}$","$F = 23.04 \\times 10^{-29}$ N",
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()


class Ex14(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 1.4 :Coulomb's law for electrostatic force between two point charges and Newton's law for gravitational force between two stationary point masses, both have inverse-square dependence on the distance between the charges and masses respectively. \\textbf{(a)} Compare the strength of these forces by determining the ratio of their magnitudes (i) for an electron and a proton and (ii) for two protons. (b) Estimate the accelerations of electron and proton due to the electrical force of their mutual attraction when they are $1 \AA (= 10^{-10}$m) apart? ($m_p = 1.67 \\times 10^{-27}$ kg, $m_e = 9.11 \\times 10^{-31}$ kg)}",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        self.play(ex_title.animate.scale(0.55).to_edge(UL))
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))

        sol = BulletedList("(a) (i)  for an electron and a proton:","$q_1=q_2 = e$ and $m_1 = m_e,\ m_2=m_p$", 
                           ' $\\dfrac{F_e}{F_g}=\\dfrac{\\dfrac{1}{4\pi\epsilon_0}\\dfrac{e^2}{r^2}}{G\\dfrac{m_em_p}{r^2}}=\\dfrac{1}{4\pi\epsilon_0}\\dfrac{e^2}{G m_em_p}$',
                           "$\\dfrac{F_e}{F_g}= \\dfrac{9\\times 10^{9} \\times 1.6\\times 10^{-19}\\times 1.6 \\times 10^{-19} }{6.67 \\times 10^{-11}\\times 9.11\\times 10^{-31}\\times 1.67\\times  10^{-27}}$","$\\dfrac{F_e}{F_g}=2.27\\times 10^{39}\\approx 10^{39}$",
                           dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList(" (a) (ii)  for two protons:","$q_1=q_2 = e$ and $m_1=m_2 =m_p$", 
                           ' $\\dfrac{F_e}{F_g}=\\dfrac{\\dfrac{1}{4\pi\epsilon_0}\\dfrac{e^2}{r^2}}{G\\dfrac{m_pm_p}{r^2}}=\\dfrac{1}{4\pi\epsilon_0}\\dfrac{e^2}{G m_pm_p}$',
                           "$\\dfrac{F_e}{F_g}= \\dfrac{9\\times 10^{9} \\times 1.6\\times 10^{-19}\\times 1.6 \\times 10^{-19} }{6.67 \\times 10^{-11}\\times 1.67\\times 10^{-27}\\times 1.67\\times  10^{-27}}$","$\\dfrac{F_e}{F_g}=1.24\\times 10^{36}\\approx 10^{36}$",dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        line = Line(sol2.get_top(),sol2.get_bottom(),color=RED).next_to(sol,RIGHT)
        g2=Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()
        
        self.play(FadeOut(g2))
        self.next_slide()
        sol3 = BulletedList("(b) Given :  $q_1=q_2=e$ and $r=10^{-10} $ m", 
                           ' Find: Acceleration of electron $(a_e)$ and \\\\ proton ($a_p$) due to electric force (F)',
                           "$F_e=F_p = \\dfrac{1}{4\pi\epsilon_0}\\dfrac{e\\times e}{r^2}$",
                           "$F_e=F_p=\\dfrac{9\\times 10^{9} \\times 1.6\\times 10^{-19}\\times 1.6 \\times 10^{-19} }{(10^{-10})^2}$",
                           dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        sol4 = BulletedList(" $F_e=F_p=23.04\\times 10^{-9}$ N", 
                           "Now, using  $F_e=m_ea_e$ acceleration of electron", "$a_e=\\dfrac{F_e}{m_e}=\\dfrac{23.04\\times 10^{-9}}{9.11\\times 10^{-31}}=2.53\\times 10^{22}\ ms^{-2}$ ",
                           "Similarly, acceleration of proton:","$a_p=\\dfrac{F_p}{m_p}=\\dfrac{23.04\\times 10^{-9}}{1.67\\times 10^{-27}}=13.79\\times 10^{18}\ ms^{-2}$",dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        line2 = Line(sol3.get_top(),sol3.get_bottom(),color=RED).next_to(sol3,RIGHT)
        g2=Group(sol3,line2,sol4).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol3:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line2))

        for item in sol4:
            self.play(Write(item))
            self.next_slide()
        

class Ex15(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 1.5 : A charged metallic sphere A is suspended by a nylon thread. Another charged metallic sphere B held by an insulating handle is brought close to A such that the distance between their centres is 10 cm, as shown in Fig. 1.7(a). The resulting repulsion of A is noted (for example, by shining a beam of light and measuring the deflection of its shadow on a screen). Spheres A and B are touched by uncharged spheres C and D respectively, as shown in Fig. 1.7(b). C and D are then removed and B is brought closer to A to a distance of 5.0 cm between their centres, as shown in Fig. 1.7(c). What is the expected repulsion of A on the basis of Coulomb's law? Spheres A and C and spheres B and D have identical sizes. Ignore the sizes of A and B in comparison to the separation between their centres.}",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title),run_time=12)
        self.next_slide()
        img1 = ImageMobject("q1a.png").scale(0.55)
        img2 = ImageMobject("q1b.png").scale(0.55)
        img3 = ImageMobject("q1c.png").scale(0.55)
        g1=Group(img1,img2,img3).arrange(DOWN,buff=0.1).next_to(ex_title,RIGHT).to_corner(RIGHT)
        self.play(ex_title.animate.scale(0.55).to_edge(UL))
        self.next_slide()
        self.play(FadeIn(img1))
        self.next_slide()
        self.play(FadeIn(img2))
        self.next_slide()
        self.play(FadeIn(img3))
        self.play(g1.animate().scale(0.55).next_to(ex_title,RIGHT).to_corner(RIGHT))
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN,buff=0.1).to_edge(LEFT).scale(0.6)
        self.play(Write(sol_label))

        sol = BulletedList('Let, $q_1\\rightarrow$ initial charge on A', ' $q_2\\rightarrow$ initial charge on B', ' $r = 10 \ cm\\rightarrow$ initial seperation b/w A and B',
                           '$\\therefore$ Initial Force $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$', "Now, $q'_1 = \\dfrac{q_1}{2}\\rightarrow$  charge on A after touching ",
                           dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList(" $q'_2 = \\dfrac{q_2}{2}\\rightarrow$  charge on B after touching ", " $r' =\\dfrac{r}{2}= 5 \ cm\\rightarrow$ final seperation b/w A and B",
                            "$\\therefore$ Final Force $F' = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q'_1q'_2}{r'^2}= \\dfrac{1}{4\pi \epsilon_0}\\dfrac{\\dfrac{q_1}{2}\\dfrac{q_2}{2}}{\\left(\\dfrac{r}{2}\\right)^2}=\\dfrac{1}{4\pi \epsilon_0} \\dfrac{\\dfrac{q_1q_2}{4}}{\\dfrac{r^2}{4}}$","$F' = \\dfrac{1}{4\pi \epsilon_0} \\dfrac{q_1q_2}{r^2}=F$",dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        line = Line(sol2.get_top(),sol2.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()

class Ex16(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 12 : Two point charges $q_1$ and $q_2$ exert a force $F$ on each other when kept certain distance apart. If the charge on each particle is halved and  the distance between the two particles is doubled, then the new force between the two particles would be }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8).shift(0.5*UP)

        op = VGroup(Tex('(a) $\\dfrac{F}{2}$').scale(0.7),Tex('(b) $\\dfrac{F}{4}$').scale(0.7),Tex('(c) $\\dfrac{F}{8}$ ').scale(0.7),Tex('(d) $\\dfrac{F}{16}$').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.next_slide()
        self.play(op.animate().scale(0.8).shift(0.5*UP))
        sol_label =Tex('Solution :', color=ORANGE).next_to(op,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList('Let, $q_1\\rightarrow$ initial charge ', ' $q_2\\rightarrow$ initial charge', ' $r \\rightarrow$ initial seperation',
                           '$\\therefore$ Initial Force $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$', "Now, $q'_1 = \\dfrac{q_1}{2}\\rightarrow$  charge is halved ",
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN,buff=0.1).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList(" $q'_2 = \\dfrac{q_2}{2}\\rightarrow$  charge is halved ", " $r' =2r \\rightarrow$ distance is doubled",
                            "$\\therefore$ Final Force $F' = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q'_1q'_2}{r'^2}= \\dfrac{1}{4\pi \epsilon_0}\\dfrac{\\dfrac{q_1}{2}\\dfrac{q_2}{2}}{\\left(2r\\right)^2}=\\dfrac{1}{4\pi \epsilon_0} \\dfrac{\\dfrac{q_1q_2}{4}}{4r^2}$","$F' = \\dfrac{1}{4\pi \epsilon_0} \\dfrac{q_1q_2}{16r^2}=\\dfrac{F}{16}$",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN,buff=0.1).to_corner(LEFT).shift(RIGHT)
        line = Line(sol2.get_top(),sol2.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[3]))

class Ex17(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 13 : Two point charges having equal charges seperated by 1 m distance experience a force of 8 N. What will be the force experienced by them, if they are held in water, at the same distance? (Given, K$_{water}=80$) }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)

        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))

        sol = BulletedList("Given $F_{air}= 8$ N and Dielectric constant of water $K_{water}=80$" ,"Find : $F_{water}= ?$",'We know that $\\dfrac{F_{air}}{F_{medium}}=K_{medium}$', "Here, K is the dielectric constant of the medium","$\\dfrac{8}{F_{water}}=80$","$ \\implies F_{water}=\\dfrac{8\ N}{80}=0.1$ N",
                           dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()


class Ex18(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 14: Two same balls having equal positive charge $q$ C are suspended by two insulating strings of equal lengths. What would be the effect on the force when a plastic sheet is inserted between the two? }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList("From Coulomb's law, electrostatic force between the two charged boides in a medium," ,
                           "$F_{medium}=\\dfrac{1}{4\pi\epsilon}\\dfrac{q_1q_2}{r^2}=\\dfrac{1}{4\pi\epsilon_0 K}\\dfrac{q_1q_2}{r^2} \quad (\\because \\dfrac{\epsilon}{\epsilon_0}=K)$"
                           , "Where, K is the dielectric constant of the medium", "For vacuum, $K=1$", "for plastic, $K>1$","$\\therefore$ after insertion of plastic sheet, the force between the two charge balls will reduce.",
                           dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

class Ex19(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Exercise 1.12: (a) Two insulated charged copper spheres A and B have their centres separated by a distance of 50 cm. What is the mutual force of electrostatic repulsion if the charge on each is $6.5 \\times 10^{-7}$ C? The radii of A and B are negligible compared to the distance of separation.\\\\ (b) What is the force of repulsion if each sphere is charged double the above amount, and the distance between them is halved?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList("Given: : $q_1 = q_2 =6.5 \\times 10^{-7} $C" ," $r = 50 \ cm=5\\times 10^{-1}\ m$",
                           "Using  Coulomb's Law $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$","$F = 9\\times 10^9 \ Nm^2C^{-2} \\times \\dfrac{6.5\\times 10^{-7}\\times 6.5\\times 10^{-7}\ C^2}{(5\\times 10^{-1}\ m)^2\ }$",
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList("$F = 9\\times 10^9 \\times \\dfrac{6.5\\times 6.5\\times 10^{-14}}{25\\times 10^{-2}}\ N$",
                           "$F = 15.21 \\times 10^{-3}\ N$","(b) $F' = \dfrac{1}{4\pi\epsilon_0}\\dfrac{2q_1\\times 2q_2}{\\left(\\dfrac{r}{2}\\right)^2}= \dfrac{1}{4\pi\epsilon_0}\\dfrac{4q_1q_2}{\\dfrac{r^2}{4}}$","$F' = 16 F$",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        line = Line(sol.get_top(),sol.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()

class Ex20(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Exercise 1.13: Suppose the spheres A and B in Exercise 1.12 have identical sizes. A third sphere of the same size but uncharged is brought in contact with the first, then brought in contact with the second, and finally removed from both. What is the new force of repulsion between A and B?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList("Given : $q_1 = q_2 =q=6.5 \\times 10^{-7} $C" ," $r = 50 \ cm=5\\times 10^{-1}\ m$",
                           "From previous question $F = 15.21 \\times 10^{-3}\ N$","New charge on A  and C after touching both sphere ", " $q'_1=q'_3=\\dfrac{q}{2}$",
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList("New charge on B after touching sphere C", "$q'_2=\\dfrac{q_2+q'_3}{2}=\\dfrac{q+\\dfrac{q}{2}}{2}=\\dfrac{3q}{4}$","New force between A and B", "$F' = \dfrac{1}{4\pi\epsilon_0}\\dfrac{q'_1\\times q'_2}{r^2}= \dfrac{1}{4\pi\epsilon_0}\\dfrac{\\dfrac{q}{2}\\times \\dfrac{3q}{4}}{r^2}= \\dfrac{3}{8} F$","$F' =\\dfrac{3}{8}\\times 15.21\\times 10^{-3} N=5.7\\times 10^{-3}\ N$",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        line = Line(sol2.get_top(),sol2.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()



class Ex21(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 15: Five balls marked $a$ to $e$ are suspended using separated threads. Pair $(b,\ c)$ and $(d,\ e)$ show electrostatic repulsion while pairs $(a,\ b),\ (c,\ e)$ and $(a,\ e)$ show electrostatic attraction. The ball marked $a$ must be }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) Negatively charged').scale(0.7),Tex('(b) positively charged ').scale(0.7),Tex('(c) Uncharged').scale(0.7),Tex('(d) Any of the above is possible').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        sol_label =Tex('Solution :', color=ORANGE).next_to(op,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList('$\\because$  $(b,\ c)$ repell each other they have same charge ', ' $\\because$  $(d,\ e)$ repell each other they have same charge ',
                           '$(\ b,\ c,\ d$ and $e)$ all are charged particles. ', '$\\because$  $(c,\ e)$ attract each other they have opposite charge ',
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN,buff=0.1).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList(" But, $e$ and $b$  both  are oppositely\\\\ charged and attracts $a$ ", " This is only possible when $a$ is neutral",
                            "They are attracting due to indction.",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN,buff=0.1).to_corner(LEFT).shift(RIGHT)
        line = Line(sol.get_top(),sol.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[2]))


class Ex22(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 16: Plot a graph showing the variation of magnitude of Coulomb's force (F) versus $\\dfrac{1}{r^2}$, where $r$ is the distance between the two charges of each pair of charges $(1\ \mu C,\ 2\ \mu C)$ and $(1\ \mu C,\ -3\ \mu C)$. Interpret the graphs obtained }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))


class Super(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(Group(list[6],list[7])))
        self.play(Circumscribe(Group(list[7],list[7])))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        super_title = Title("Forces between multiple charges and Superposition Principle", color=GREEN)
        self.play(ReplacementTransform(title,super_title))
        self.next_slide()
        Super_lbl = Tex('The superposition principle :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(Write(Super_lbl))
        ax = Axes(x_range=[0,6],y_range=[0, 6],x_length=10,y_length=8)
        q1 = Dot(ax.coords_to_point(5,5),color=YELLOW).scale(2.5)
        q2 = Dot(ax.coords_to_point(1,3),color=YELLOW).scale(2.5)
        q3 = Dot(ax.coords_to_point(5,2),color=YELLOW).scale(2.5)
        q1_text=Tex('$q_1$').next_to(q1,DR,buff=0.2).scale(1.5)
        q2_text=Tex('$q_2$').next_to(q2,UP,buff=0.2).scale(1.5)
        q3_text=Tex('$q_3$').next_to(q3,RIGHT,buff=0.2).scale(1.5)
        vector_1 = Arrow(ax.coords_to_point(0,0),ax.coords_to_point(5,5),buff=0,color=BLUE)
        vector_2 = Arrow(ax.coords_to_point(0,0),ax.coords_to_point(1,3),buff=0,color=BLUE)
        vector_3 = Arrow(ax.coords_to_point(0,0),ax.coords_to_point(5,2),buff=0,color=BLUE)
        v1_lbl = MathTex('\\vec{r}_1').scale(1.5).move_to(ax.coords_to_point(3.8,3))
        v2_lbl = Tex('$\\vec{r}_{2}$').scale(1.5).move_to(ax.coords_to_point(0.2,2))
        v3_lbl = Tex('$\\vec{r}_{3}$').scale(1.5).move_to(ax.coords_to_point(3.8,1))
        vector_12 = Arrow(ax.coords_to_point(1,3),ax.coords_to_point(5,5),buff=0,color=RED)
        v12_lbl = MathTex('\\vec{r}_{12 } ').scale(1.5).move_to(ax.coords_to_point(3.5,5.3))
        vector_13 = Arrow(start=ax.coords_to_point(5,2),end=ax.coords_to_point(5,5),buff=0,color=RED)
        v13_lbl = MathTex('\\vec{r}_{13 } ').scale(1.5).next_to(vector_13,RIGHT)
        f12_arrow = Arrow(start=q1.get_center(),end=q1.get_center()+[3,1.5,0],buff=0,color=GREEN_D) 
        f13_arrow = Arrow(start=q1.get_center(),end=q1.get_center()+[0,3,0],buff=0,color=PINK)
        f12_lbl = Tex('$\\vec{F}_{12}$').scale(1.5).move_to(ax.coords_to_point(6,5))
        f13_lbl = Tex('$\\vec{F}_{13}$').scale(1.5).next_to(f13_arrow,LEFT)
        f12_line = DashedLine(start=q1.get_center()+[3,1.5,0],end=q1.get_center()+[3,4.5,0],buff=0,color=PINK)
        f13_line = DashedLine(start=q1.get_center()+[3,4.5,0],end=q1.get_center()+[0,3,0],buff=0,color=GREEN_D)
        f1_arrow = Arrow(start=q1.get_center(),end=q1.get_center()+[3,4.5,0],buff=0,color=YELLOW) 
        f1_lbl = Tex('$\\vec{F}_{1}$').scale(1.5).move_to(ax.coords_to_point(6.2,6.5))
        g1 = VGroup(ax,q1,q2,q3,q1_text,q2_text,q3_text,vector_1,vector_2,v1_lbl,v2_lbl,vector_12,v12_lbl,f12_arrow,f13_arrow,f12_lbl,f13_lbl,vector_3,v3_lbl,vector_13,v13_lbl,f12_line,f13_line,f1_arrow,f1_lbl).scale(0.45).next_to(Super_lbl,DOWN).to_edge(RIGHT)
        

        list3 =  LatexItems( r"\item This pricnciple tells us that if charge $q_1$ is acted upon by several charges $q_2,\ q_3, ......, \ q_n$, then the force on $q_1$ can be found out by calculating separately the force $\vec{F}_{12},\ \vec{F}_{13},\ ...,\ \vec{F}_{1n}$ exerted by $q_2,\ q_3,\ ...,\ q_n$, respenctively on $q_1$, then adding these forces vectorially.",
                            r"\item Their resultant $\vec{F}_1$ is that total force on $q_1$ due to the collection of charges.\[\vec{F}_1=\vec{F}_{12}+\vec{F}_{13}+....\vec{F}_{1n}\]",
                            itemize="itemize" ,page_width="25em").scale(0.7).next_to(Super_lbl,DOWN).to_edge(LEFT)
        self.next_slide()
        g2=Group(list3,g1).arrange(RIGHT,buff=0.15).next_to(Super_lbl,DOWN).shift(RIGHT).to_corner(LEFT)
        for item in list3:
            self.play(Write(item))
            self.next_slide()
        self.play(FadeIn(q1,q2,q3),Write(q1_text),Write(q2_text),Write(q3_text))
        self.next_slide()
        self.play(Create(VGroup(ax,vector_1,vector_2,vector_3,v1_lbl,v3_lbl,v2_lbl)))
        self.next_slide()
        self.play(Create(VGroup(vector_12,v12_lbl)))
        self.next_slide()
        self.play(Create(VGroup(vector_13,v13_lbl)))
        self.next_slide()
        self.play(Create(VGroup(f12_arrow)),Write(f12_lbl))
        self.next_slide()
        self.play(Create(VGroup(f13_arrow)),Write(f13_lbl))
        self.next_slide()
        self.play(Create(VGroup(f1_arrow,f13_line,f12_line)),Write(f1_lbl))
        self.next_slide()
        list3.scale(0.7)
        g1.scale(0.7)
        list4 =  LatexItems( r"\item\[ \vec{F}_1=\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_2}{|\vec{r}_{12}|^2} \hat{r}_{12}+\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_3}{|\vec{r}_{13}|^2} \hat{r}_{13}+....+\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_n}{|\vec{r}_{1n}|^2 }\hat{r}_{1n}\]",r"\item \[\vec{F}_{1}=\dfrac{q_1}{4\pi\epsilon_0}\left[\dfrac{q_2}{|\vec{r}_{12}|^2} \hat{r}_{12} + \dfrac{q_3}{|\vec{r}_{13}|^2} \hat{r}_{13}+....+\dfrac{q_n}{|\vec{r}_{1n}|^2 }\hat{r}_{1n} \right]\]",r"\item\[\vec{F}_1=\dfrac{q_1}{4\pi\epsilon_0}\left[\sum_{i=2}^{n} \dfrac{q_i}{|\vec{r}_{1i}|^2} \hat{r}_{1i}\right]\]",
                            itemize="itemize" ,page_width="30em").scale(0.7).next_to(g2,DOWN).scale(0.8).align_to(g2,LEFT)
        
        self.play(FadeOut(super_title))
        g3 = Group(g1,list4).arrange(DOWN).next_to(list3,RIGHT)
        Group(list3,g3).arrange(RIGHT)
        for item in list4:
            self.play(Write(item))
            self.next_slide()

class Ex23(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 17: Point charges $q_1 = 50\ \mu$ C and $q_2 = -25\ \mu$C are placed 1.0 m apart. What is the force on a third charge $q_3 = 20\ \mu$C placed midway between $q_1$ and $q_2$ ? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))

class Ex24(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 18: Point charges $Q_1 = 2.0\ \mu$C and $Q_2 = 4.0\ \mu$C are located at $\\vec{r}_1=\\left( 4\hat{i}-2\hat{j}+5\hat{k}\\right)$m and  $\\vec{r}_2=\\left( 8\hat{i}+5\hat{j}-9\hat{k}\\right)$m. What is the force of $Q_2$ on $Q_1$ ? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))

class Ex25(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 19: A charge $q = 2.0\ \mu$C is placed at the point P shown below. What is the force on $q$? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        img = ImageMobject('ex25.png').scale(0.6).next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.play(FadeIn(img))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(img,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))

class Ex26(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 20: Two charges $+3\ \mu$C and $+12\ \mu$C are fixed 1 m apart, with the second one to the right. Find the magnitude and direction of the net force on a $-2$ nC charge when placed at the following locations: (a) halfway between the two (b) half a meter to the left of the $+3\ \mu$C charge (c) half a meter above the $+12\ \mu$C charge in a direction perpendicular to the line joining the two fixed charges? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))

class Ex27(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 21: The charges $q_1 = 2.0 \\times 10^{-7}$ C, $q_2 = -4.0 \\times 10^{-7}$ C, and $q_3 = -1.0 \\times 10^{-7}$ C are placed at the corners of the triangle shown below. What is the force on $q_1$ ? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        img = ImageMobject('ex27.png').scale(0.5).next_to(ex_title,DR).to_edge(RIGHT)
        self.play(Write(ex_title))
        self.play(FadeIn(img))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
