from manimlib import *
from custom.util import get_svg_path, shift_mobject
from custom.gen_util.custom_anim import shift_from_current_position
import numpy as np

class Outro(Scene):
    def construct(self):
        self.do_graph_animations()

        self.wait(1)

        headerr = Text("More applications of consumer surplus include:").scale(0.5)

        more_applications = VGroup(
            Text("- Solving the water-diamond paradox (paradox of value)"),
            Text("- Analyzing effects of subsidies and excise taxes"),
            Text("- Applications in international trade"),
            Text("- Analyzing living standards"),
            Text("- Making choices in public policy"),
            Text("- Probably many more..."),
        ).arrange(DOWN, center=False, aligned_edge=LEFT).scale(0.3)

        tt = VGroup(headerr, more_applications).arrange(DOWN)

        self.play(ShowCreation(headerr))

        for i in more_applications:
            self.play(ShowCreation(i), run_time=1.1)

        self.wait(2)

        self.play(Uncreate(tt))

        thanks = Text("Thanks for listening!").scale(0.6)

        self.wait(1)

        self.play(ShowCreation(thanks))

        self.wait(1)

        self.play(Uncreate(thanks))

        self.wait(1)
        # much more entails:
        # - solving the water-diamond paradox (paradox of value)
        # - analyzing effects of subsidies and excise taxes
        # - applications in international trade
        # - analyzing living standards
        # - making choices in public policy

        #end

    def do_graph_animations(self):
        AXES_WH = 4.5 # axes width and height are the same cuz economics
        EQ_QTY = 3
        EQ_PRICE = 4
        X_RANGE_UPPER_BOUND = 6
        X_RANGE_LOWER_BOUND = 0

        axes = Axes(
            (0, 7), (0, 8), height=AXES_WH, width=AXES_WH
        )

        demand_graph = axes.get_graph(
            lambda x : -x + 7,
            x_range = (X_RANGE_LOWER_BOUND, X_RANGE_UPPER_BOUND),
            color = RED,
            )
        demand_graph_label = axes.get_graph_label(demand_graph, "D")
        demand_graph_label_monopoly = axes.get_graph_label(demand_graph, "D=AR")

        supply_graph = axes.get_graph(
            lambda x : x + 1,
            x_range = (X_RANGE_LOWER_BOUND, X_RANGE_UPPER_BOUND),
            color = BLUE,
            )
        supply_graph_label = axes.get_graph_label(supply_graph, "S")
        shift_mobject(supply_graph_label, [1, 0, 0])
        supply_graph_label_monopoly = axes.get_graph_label(supply_graph, "S=MC")
        shift_mobject(supply_graph_label_monopoly, [1.9, 0, 0])
        bounds_graph_tax = axes.get_graph(
            lambda x : 5,
            x_range=(X_RANGE_LOWER_BOUND-1, X_RANGE_UPPER_BOUND)
        )

        bounds_graph_tax_low = axes.get_graph(
            lambda x : 3,
            x_range=(X_RANGE_LOWER_BOUND-1, X_RANGE_UPPER_BOUND)
        )

        bounds_graph_floor = axes.get_graph(
            lambda x : 5,
            #x_range=(X_RANGE_LOWER_BOUND-1, X_RANGE_UPPER_BOUND)
        )
        bounds_floor_label = axes.get_graph_label(bounds_graph_floor, "P_{Floor}")

        bounds_graph_ceil = axes.get_graph(
            lambda x : 2,
            #x_range=(X_RANGE_LOWER_BOUND, X_RANGE_UPPER_BOUND)
        )
        bounds_ceil_label = axes.get_graph_label(bounds_graph_ceil, "P_{Ceil}")

        axes_p = Text("P").scale(0.6).next_to(axes, LEFT)
        axes_q = Text("Q").scale(0.6).next_to(axes, RIGHT)

        shift_mobject(axes_p, [0, axes.get_height()/ 2, 0])
        shift_mobject(axes_q, [0, - axes.get_height()/ 2, 0])

        self.play(ShowCreation(axes),
            ShowCreation(axes_p),
            ShowCreation(axes_q),
        )

        self.play(
            ShowCreation(demand_graph), ShowCreation(demand_graph_label),
            ShowCreation(supply_graph), ShowCreation(supply_graph_label),
        )

        original_group = VGroup(
            axes,
            demand_graph,
            demand_graph_label,
            supply_graph,
            supply_graph_label,
            bounds_graph_floor,
            bounds_floor_label,
            axes_p,
            axes_q
        )

        shifty = 3

        p_cf_copy = VGroup(
            axes.copy(),
            demand_graph.copy(),
            demand_graph_label.copy(),
            supply_graph.copy(),
            supply_graph_label.copy(),
            bounds_graph_ceil.copy(),
            bounds_ceil_label.copy(),
            axes_p.copy(),
            axes_q.copy()
        )
        ceil_qty = 1

        dx_const = 0.02

        price_ceil_cs_area = p_cf_copy[0].get_riemann_rectangles(
            p_cf_copy[1],
            bounded = p_cf_copy[5],
            x_range=(0, ceil_qty),
            dx=dx_const,
            stroke_width=0,
            stroke_color=BLACK,
            fill_opacity=0.5,colors=("#FF4242", "#FF0022")
        )

        price_ciel_ps_area = p_cf_copy[0].get_riemann_rectangles(
            p_cf_copy[5],
            bounded = p_cf_copy[3],
            x_range=(0, ceil_qty),
            dx=dx_const,
            stroke_width=0,
            stroke_color=BLACK,
            fill_opacity=0.5,colors=("#0062ff", "#1f75ff")
        )

        ar_lef_pca = np.add(price_ciel_ps_area.get_center(), [1, -0.5, 0])
        label_pca = Text("Producer surplus").move_to(ar_lef_pca)
        shift_mobject(label_pca, [0.5, 0,0])

        arrow_to_ciel_ps = Arrow(ar_lef_pca, price_ciel_ps_area.get_center())

        price_ciel_dwl_area = axes.get_riemann_rectangles(
            p_cf_copy[1],
            bounded = p_cf_copy[3],
            x_range=(ceil_qty, EQ_QTY),
            dx=dx_const,
            stroke_width=0,
            stroke_color=BLACK,
            fill_opacity=0.5,colors=(BLACK, BLACK)
        )

        p_cf_copy.add(price_ceil_cs_area)
        p_cf_copy.add(price_ciel_ps_area)
        p_cf_copy.add(price_ciel_dwl_area)
        p_cf_copy.add(arrow_to_ciel_ps)

        p_cf_copy.move_to([shifty, 0,0])

        p_cf_copy.remove(price_ceil_cs_area)
        p_cf_copy.remove(price_ciel_ps_area)
        p_cf_copy.remove(price_ciel_dwl_area)
        p_cf_copy.remove(arrow_to_ciel_ps)

        #.move_to([shifty - 1.6, 0.5,0])

        self.play(
            ShowCreation(bounds_graph_floor),
            ShowCreation(bounds_floor_label),
            shift_from_current_position(original_group, [-shifty, 0, 0]),
            ShowCreation(p_cf_copy)
        )

        self.wait(2)

        price_floor_cs_area = axes.get_riemann_rectangles(
            demand_graph,
            bounded = bounds_graph_floor,
            x_range=(0, 2),
            dx=dx_const,
            stroke_width=0,
            stroke_color=BLACK,
            fill_opacity=0.5,colors=("#FF4242", "#FF0022")
        )

        price_floor_ps_area = axes.get_riemann_rectangles(
            bounds_graph_floor,
            bounded = supply_graph,
            x_range=(0, 2),
            dx=dx_const,
            stroke_width=0,
            stroke_color=BLACK,
            fill_opacity=0.5,colors=("#0062ff", "#1f75ff")
        )

        ar_lef_pfa = np.add(price_floor_ps_area.get_center(), [1, -0.5, 0])
        label_pfa = Text("Producer surplus").move_to(ar_lef_pfa)
        shift_mobject(label_pfa, [0.5, 0,0])

        arrow_to_floor_ps = Arrow(ar_lef_pfa, price_floor_ps_area.get_center())

        price_floor_dwl_area = axes.get_riemann_rectangles(
            demand_graph,
            bounded = supply_graph,
            x_range=(2, EQ_QTY),
            dx=dx_const,
            stroke_width=0,
            stroke_color=BLACK,
            fill_opacity=0.5,colors=(BLACK, BLACK)
        )

        self.play(ShowCreation(price_floor_cs_area), ShowCreation(price_ceil_cs_area), ShowCreation(price_floor_dwl_area),
        ShowCreation(price_floor_ps_area), ShowCreation(price_ciel_ps_area), ShowCreation(price_ciel_dwl_area))

        self.wait(2)

        self.play(Uncreate(price_floor_cs_area), Uncreate(price_ceil_cs_area),Uncreate(price_floor_ps_area), Uncreate(price_ciel_ps_area),
        Uncreate(price_ciel_dwl_area),Uncreate(price_floor_dwl_area) )

        self.play(
            Uncreate(p_cf_copy),
            Uncreate(bounds_floor_label),
            Uncreate(bounds_graph_floor),
            original_group.animate.move_to([shifty,0,0])
        )

        original_group.remove(bounds_graph_floor)
        original_group.remove(bounds_floor_label)

        gov_svg_file = get_svg_path("govt.svg", file = __file__)
        gov_svg = SVGMobject(gov_svg_file).rotate(180 * DEGREES).scale(1.6).move_to([-3.4, 0, 0])

        self.play(DrawBorderThenFill(gov_svg))

        sup_to_move = supply_graph.copy()

        supply_tax_graph = axes.get_graph(
            lambda x : x + 3,
            x_range = (X_RANGE_LOWER_BOUND, X_RANGE_UPPER_BOUND),
            color = BLUE,
            )


        supply_tax_graph_label = axes.get_graph_label(supply_tax_graph, "S_{Tax}")

        shift_mobject(supply_tax_graph_label, [1.3, 0,0])

        self.play(sup_to_move.animate.move_to(supply_tax_graph.get_center()))
        self.wait(1)
        self.play(ShowCreation(supply_tax_graph_label))

        self.wait(1)

        TAX_EQ_X = 2

        area_between_d_and_tax = axes.get_riemann_rectangles(
            demand_graph,
            bounded = bounds_graph_tax,
            x_range=(0, TAX_EQ_X),
            dx=dx_const,stroke_width=0, stroke_color=BLACK, fill_opacity=0.5,colors=("#FF4242", "#FF0022")
        )

        area_of_deadweight = axes.get_riemann_rectangles(
            demand_graph,
            bounded = supply_graph,
            x_range=(2, EQ_QTY),
            dx=dx_const,stroke_width=0, stroke_color=BLACK, fill_opacity=0.5,colors=(BLACK, BLACK)
        )

        area_of_tax = axes.get_riemann_rectangles(
            bounds_graph_tax,
            bounded = bounds_graph_tax_low,
            x_range=(0, TAX_EQ_X),
            dx=dx_const,stroke_width=0, stroke_color=BLACK, fill_opacity=0.5,colors=("#545454", "#545454")
        )

        tax_ps_area = axes.get_riemann_rectangles(
            bounds_graph_tax_low,
            bounded = supply_graph,
            x_range=(0, TAX_EQ_X),
            dx=dx_const,
            stroke_width=0,
            stroke_color=BLACK,
            fill_opacity=0.5,colors=("#0062ff", "#1f75ff")
        )

        ar_lef_1 = np.add(tax_ps_area.get_center(), [1, -0.5, 0])
        label_pst = Text("Producer surplus").scale(0.3).move_to(ar_lef_1)
        shift_mobject(label_pst, [0.5, 0, 0])

        arrow_to_tax_ps = Arrow(ar_lef_1, tax_ps_area.get_center())

        arrow_to_tax_dwl = self.arrow_to_thing(axes, 2, 2, 3, supply_graph, demand_graph, demand_graph, "Deadweight loss",
        line_from_tip=[1.5, 0,0], label_offset = [1,0,0])

        arrow_to_tax_surplus = self.arrow_to_thing(axes, EQ_QTY, 0, 0, demand_graph, demand_graph, bounds_graph_tax, "Consumer surplus",
        line_from_tip=[1.5, 0.9,0], label_offset = [0,1,0])

        arrow_left = np.add(area_of_tax.get_center(), [-1, -1, 0])

        arrow_to_tax = Arrow(
            arrow_left, area_of_tax.get_center()
        )

        tax_text = Text("Tax revenue").scale(0.3).move_to(arrow_left)
        shift_mobject(tax_text, [-0.5, -0.25, 0])

        self.play(ShowCreation(area_between_d_and_tax), ShowCreation(area_of_deadweight), ShowCreation(arrow_to_tax_surplus[0]), ShowCreation(arrow_to_tax_surplus[1]),
        ShowCreation(arrow_to_tax_dwl[0]), ShowCreation(arrow_to_tax_dwl[1]), ShowCreation(area_of_tax), ShowCreation(arrow_to_tax),ShowCreation(tax_text),
        ShowCreation(tax_ps_area), ShowCreation(arrow_to_tax_ps),ShowCreation(label_pst),
        )

        self.wait(1)

        self.play(
            Uncreate(sup_to_move), Uncreate(supply_tax_graph_label), Uncreate(gov_svg), Uncreate(arrow_to_tax_dwl[0]), Uncreate(arrow_to_tax_dwl[1]),
            Uncreate(area_between_d_and_tax), Uncreate(area_of_deadweight), Uncreate(arrow_to_tax_surplus[0]), Uncreate(arrow_to_tax_surplus[1]), Uncreate(area_of_tax), Uncreate(arrow_to_tax),
            Uncreate(tax_text), Uncreate(tax_ps_area), Uncreate(arrow_to_tax_ps),Uncreate(label_pst),

        )

        self.play(
            original_group.animate.move_to(ORIGIN),
            ReplacementTransform(supply_graph_label, supply_graph_label_monopoly),
            ReplacementTransform(demand_graph_label, demand_graph_label_monopoly)
        )

        mr_monopoly = axes.get_graph(
            lambda x : -2 * x + 7,
            x_range = (X_RANGE_LOWER_BOUND, 3.5),
            color = RED,
            )
        mr_monopoly_label = axes.get_graph_label(demand_graph, "MR").move_to(axes.c2p(4, 1))

        mr_mc_qty = 2
        c_monopoly_surplus_lower = 5

        bounds_graph_monopoly_surplus = axes.get_graph(
            lambda x : c_monopoly_surplus_lower,
            x_range=(X_RANGE_LOWER_BOUND, mr_mc_qty)
        )

        monopoly_area_surplus = axes.get_riemann_rectangles(
            demand_graph,
            bounded = bounds_graph_monopoly_surplus,
            x_range=(0, mr_mc_qty),
            dx=dx_const,stroke_width=0, stroke_color=BLACK, fill_opacity=0.5,colors=("#FF4242", "#FF0022")
        )

        monopoly_area_deadweight = axes.get_riemann_rectangles(
            demand_graph,
            bounded = supply_graph,
            x_range=(mr_mc_qty, EQ_QTY),
            dx=dx_const,stroke_width=0, stroke_color=BLACK, fill_opacity=0.5,colors=(BLACK, BLACK)
        )

        monopoly_ps_area = axes.get_riemann_rectangles(
            bounds_graph_monopoly_surplus,
            bounded = supply_graph,
            x_range=(0, mr_mc_qty),
            dx=dx_const,
            stroke_width=0,
            stroke_color=BLACK,
            fill_opacity=0.5,colors=("#0062ff", "#1f75ff")
        )

        ar_lef = np.add(monopoly_ps_area.get_center(), [1, -0.5, 0])
        label_mm = Text("Producer surplus").scale(0.3).move_to(ar_lef)
        shift_mobject(label_mm, [0.5, 0,0])

        arrow_to_monopoly_ps = Arrow(ar_lef, monopoly_ps_area.get_center())

        self.play(ShowCreation(mr_monopoly), ShowCreation(mr_monopoly_label))

        self.wait(1)

        arrow_to_mid_monopoly_dwl = self.arrow_to_thing(axes, 2, 2, 3, supply_graph, demand_graph, demand_graph, "Deadweight loss",
        line_from_tip=[1.5, 0,0], label_offset = [1,0,0])

        arrow_monopoly_surplus = self.arrow_to_thing(axes, EQ_QTY, 0, 0, demand_graph, demand_graph, bounds_graph_monopoly_surplus, "Consumer surplus",
        line_from_tip=[1.5, 0.9,0], label_offset = [0,0.2,0])

        self.play(ShowCreation(monopoly_area_surplus), ShowCreation(monopoly_area_deadweight),
            ShowCreation(arrow_to_mid_monopoly_dwl[0]), ShowCreation(arrow_to_mid_monopoly_dwl[1]),
            ShowCreation(arrow_monopoly_surplus[0]), ShowCreation(arrow_monopoly_surplus[1]),
            ShowCreation(monopoly_ps_area), ShowCreation(arrow_to_monopoly_ps), ShowCreation(label_mm)
        )

        self.wait(1)

        self.play(Uncreate(monopoly_area_surplus), Uncreate(monopoly_area_deadweight),Uncreate(monopoly_ps_area), Uncreate(arrow_to_monopoly_ps), Uncreate(label_mm))

        self.play(Uncreate(axes), Uncreate(supply_graph),Uncreate(arrow_to_mid_monopoly_dwl[0]), Uncreate(arrow_to_mid_monopoly_dwl[1]), Uncreate(arrow_monopoly_surplus[0]), Uncreate(arrow_monopoly_surplus[1]),
        Uncreate(demand_graph),Uncreate(mr_monopoly), Uncreate(mr_monopoly_label), Uncreate(supply_graph_label_monopoly), Uncreate(demand_graph_label_monopoly),
        Uncreate(axes_p), Uncreate(axes_q)
        )



        #price floor /ceil stuff w surplus on graph
    def arrow_to_thing(self, axes, p1x, p2x, p3x, p1g, p2g, p3g, label_text, line_from_tip = [0,0,0], label_offset = [0,0,0]):
        indexer = lambda x : (axes.i2gp(p1x, p1g)[x] +  axes.i2gp(p2x, p2g)[x] + axes.i2gp(p3x, p3g)[x])/3
        centroid_center = np.array([indexer(0), indexer(1), 0])

        line_left = np.add(centroid_center, line_from_tip)


        arrow = Arrow(line_left, centroid_center)
        arrow.set_thickness(0.02)
        label = Text(label_text)
        label.scale(0.3)
        label.move_to(np.add(line_left, label_offset))

        return (label, arrow)
