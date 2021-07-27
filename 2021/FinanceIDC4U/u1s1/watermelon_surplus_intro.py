from manimlib import *
from custom.util import get_svg_path, get_png_path, shift_mobject
from custom.tables import AnimatedTable
from custom.econ_util.graphics import PriceLabel
from custom.gen_util.graphics import LabelledHead

class SurplusIntroExample(Scene):
    def construct(self):
        water_melon_image = get_svg_path("watermelon", __file__)#png

        thought_svg = get_svg_path("thinking.svg", file=__file__)
        happy_svg = get_svg_path("happyface.svg", file = __file__)

        thk_price_tag = PriceLabel("6.00").get_label_mobject()
        price_tag = PriceLabel("4.00").get_label_mobject()
        watermelon_vec = SVGMobject(water_melon_image)
        think_vec = SVGMobject(thought_svg)
        shift_mobject(think_vec, [0.5,0.9,0])
        happy_vec = SVGMobject(happy_svg)


        you_head = LabelledHead("You", True).get_head_obj()

        self.play(DrawBorderThenFill(you_head))
        self.play(you_head.animate.scale(0.65).move_to([-5.2, -2.5, 0]))
        self.play(FadeIn(think_vec.scale(3)))

        thinking_v_group = VGroup(
            thk_price_tag.scale(0.4),
            watermelon_vec.rotate(180 * DEGREES),
        ).arrange(RIGHT, buff = 0.25).move_to(think_vec.get_center())

        shift_mobject(thk_price_tag, [0, 0.75, 0])

        self.play(DrawBorderThenFill(thinking_v_group[1])) #the thought

        self.wait(0.8)

        self.play(DrawBorderThenFill(thinking_v_group[0]))

        happy_vec.rotate(-90 * DEGREES).scale(0.57).move_to(
            np.add(thinking_v_group.get_center(), [thinking_v_group.get_width() / 2, 0, 0]
        ))

        self.play(
            thinking_v_group.animate.scale(0.7).move_to(
                np.add(thinking_v_group.get_center(), [-0.87, 0, 0]
            )),
            ShowCreation(happy_vec)
        )

        self.wait(0.5)

        lob_watermelon = watermelon_vec.copy()
        lob_happy = happy_vec.copy()

        self.play(Uncreate(thinking_v_group), Uncreate(happy_vec), FadeOut(think_vec))

        loblaws_melons = VGroup(
            price_tag.scale(0.4),
            lob_watermelon,
        ).arrange(RIGHT, buff = 0.25)

        shift_mobject(price_tag, [0, 0.75, 0])

        loblaws_vg = VGroup(
            loblaws_melons,
            Text("Loblaws"),
        ).arrange(DOWN, buff = 0.5).move_to([2.75, 0, 0])

        self.play(
            you_head.animate.move_to([-2, 0, 0]).scale(2.0)
        )

        self.wait(0.2)

        self.play(
            ShowCreation(loblaws_vg), run_time=1.6
        )

        self.play(
            you_head.animate.move_to([-4, 0, 0]),
        )

        self.play(ShowCreation(lob_happy.move_to(np.add(you_head.get_center(), [you_head.get_width() / 2 + 1+ lob_happy.get_width() / 2, 0 ,0]))))

        on_screen = VGroup(
            loblaws_vg,
            lob_happy,
            you_head
        )

        self.play(on_screen.animate.move_to(
            np.add(on_screen.get_center(), [0, 2.6, 0])
            ).scale(0.66)
        )

        formula_vgroup = VGroup(
            Tex("C_{Surplus}"),
            Tex("{{=}}"),
            Tex("P_{Willing}"),
            Tex("{{-}}"),
            Tex("P_{Market}")
        ).arrange(RIGHT, buff = 0.3)

        final_surplus_calc_vgroup = VGroup(
            Tex("{{\$2.00}}"),
            Tex("{{=}}"),
            Tex("{{\$6.00}}"),
            Tex("{{-}}"),
            Tex("{{\$4.00}}")
        ).arrange(RIGHT, buff = 0.3)

        shift_mobject(final_surplus_calc_vgroup, [0, -1, 0])

        res_grp = VGroup(
            Tex("C_{Surplus}"),
            Tex("{{=}}"),
            Tex("{{\$2.00}}"),
        ).arrange(RIGHT, buff = 0.3)

        shift_mobject(res_grp, [0, -2, 0])

        self.play(ShowCreation(formula_vgroup[2]))
        self.wait(0.7)
        self.play(ShowCreation(formula_vgroup[3]))
        self.wait(0.7)
        self.play(ShowCreation(formula_vgroup[4]))
        self.wait(1.3)

        self.play(ShowCreation(formula_vgroup[0]), ShowCreation(formula_vgroup[1]))

        PAD = 0.06
        final_answ_box = Rectangle(formula_vgroup[0].get_width()+ 2 * PAD, formula_vgroup[0].get_height() + 2 * PAD).set_stroke(width=0.75).move_to(formula_vgroup[0].get_center())

        self.play(ShowCreation(final_answ_box))
        self.wait(0.065)
        self.play(Uncreate(final_answ_box))

        self.wait(2.5)

        self.play(
            TransformMatchingTex(formula_vgroup[2].copy(), final_surplus_calc_vgroup[2])
        )

        self.play(
            TransformMatchingTex(formula_vgroup[4].copy(), final_surplus_calc_vgroup[4])
        )

        self.play(
            TransformMatchingTex(formula_vgroup[0].copy(), final_surplus_calc_vgroup[0])
        )

        self.play(
            TransformMatchingTex(formula_vgroup[1].copy(), final_surplus_calc_vgroup[1]),
            TransformMatchingTex(formula_vgroup[3].copy(), final_surplus_calc_vgroup[3])
        )

        self.play(
            TransformMatchingTex(final_surplus_calc_vgroup[0].copy(), res_grp[2]),
            TransformMatchingTex(formula_vgroup[0].copy(), res_grp[0]),
            ShowCreation(res_grp[1])
        )

        self.wait(3.75)

        PAD = 0.06
        final_answ_box = Rectangle(res_grp.get_width()+ 2 * PAD, res_grp.get_height() + 2 * PAD).set_stroke(width=0.75).move_to(res_grp.get_center())

        self.play(ShowCreation(final_answ_box))
        self.wait(0.065)
        self.play(Uncreate(final_answ_box))

        self.wait(0.065)

        self.wait(1)

        self.play(
            Uncreate(formula_vgroup),
            Uncreate(final_surplus_calc_vgroup),
            Uncreate(res_grp),
            Uncreate(on_screen),
        )

        #go to store --> happy

        #illustrate surplus math
