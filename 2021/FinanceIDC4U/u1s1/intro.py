from manimlib import *
from custom.util import get_svg_path

class Introduction(Scene):
    def construct(self):
        title_text = Text(
            "What is a consumer surplus?",
            t2g = {"consumer surplus": ("#FF4242", "#FF0022")},
            t2w = {"consumer surplus": BOLD}
        )

        p = lambda x : np.add(title_text.get_center(), [(title_text.get_width() / 2 if x else -title_text.get_width() / 2), -title_text.get_height() / 2, 0])

        define_text = VGroup(Text(
            "A consumer surplus occurs in a market when the price a consumer pays",
            t2g = {"consumer surplus": ("#FF4242", "#FF0022")},
            t2w = {"consumer surplus": BOLD,
                    "the price a consumer pays": BOLD
            },
        ),
            Text(
            "for a good or service is less than the price that they were",
            t2w = {"less than": BOLD}
            )

            ,
            Text(
                "originally willing and able to pay.",
                t2w = {"originally": BOLD}
            )
        ).arrange(DOWN, center=False, aligned_edge=LEFT)

        cons_actual_text = Text("$$$ Actually paid by consumers")
        less_than = Tex("{{<}}")
        cons_willing_text = Text("$$$ Consumers are willing to pay")

        explain_lines = VGroup(
            cons_actual_text,
            less_than.scale(1.2),
            cons_willing_text
        ).arrange(RIGHT, buff = 0.5)

        move_relative_to_current = lambda object, vec_to_add : np.add(object.get_center(), vec_to_add)

        explain_lines.scale(0.35).move_to(move_relative_to_current(explain_lines, [0, -0.3, 0]))
        define_text.move_to(move_relative_to_current(define_text, [0, 2.25, 0])).scale(0.4)

        SHIFT_COIN_REL_TO_LINE = -1.65

        coinstack_path = get_svg_path("coinstack.svg", file=__file__)

        money_svg_l = SVGMobject(coinstack_path)
        money_svg_l.move_to(np.add(cons_actual_text.get_center(), [-0.5, SHIFT_COIN_REL_TO_LINE, 0]))
        money_svg_l.scale(0.6).set_style(fill_opacity = 0)

        money_svg_r = [
        SVGMobject(coinstack_path).scale(0.6),
        SVGMobject(coinstack_path).move_to(np.add(cons_willing_text.get_center(), [0.5, SHIFT_COIN_REL_TO_LINE, 0])).scale(0.6),
        SVGMobject(coinstack_path).scale(0.6)]

        for money in money_svg_r:
            money.set_style(fill_opacity = 0)

        C_SHIFT_AMT = 1.4

        money_svg_r = VGroup(
            money_svg_r[0].move_to(np.add(money_svg_r[1].get_center(), [-C_SHIFT_AMT, 0, 0])),
            money_svg_r[1],
            money_svg_r[2].move_to(np.add(money_svg_r[1].get_center(), [C_SHIFT_AMT, 0, 0]))
        )

        self.play(Write(title_text), run_time=3)

        self.play(title_text.animate.to_edge(TOP, buff = 0.15), run_time=0.6)

        title_underline = Line(p(False), p(True))
        self.play(ShowCreation(title_underline), run_time=0.25)

        self.play(Write(define_text), run_time=6)
        self.play(Write(cons_actual_text), Write(less_than), Write(cons_willing_text))

        self.play(DrawBorderThenFill(money_svg_l), DrawBorderThenFill(money_svg_r))

        ANIM_WEIGHT = -2

        anim = lambda svg, arr: svg.animate.move_to(move_relative_to_current(svg, arr))
        diff = 0.15
        back = 0.05

        self.play(
            anim(money_svg_l, [0, ANIM_WEIGHT * diff, 0]),
            anim(money_svg_r, [0, ANIM_WEIGHT * -diff, 0])
        )

        self.play(
            anim(money_svg_l, [0, ANIM_WEIGHT * -back, 0]),
            anim(money_svg_r, [0, ANIM_WEIGHT * back, 0])
        )

        self.play(
            anim(money_svg_l, [0, ANIM_WEIGHT * back, 0]),
            anim(money_svg_r, [0, ANIM_WEIGHT * -back, 0])
        )

        self.wait(1)

        self.play(
            Uncreate(title_text),
            Uncreate(title_underline),
            Uncreate(define_text),
            Uncreate(explain_lines),
            Uncreate(money_svg_l),
            Uncreate(money_svg_r),
        )

        self.wait(0.7)
