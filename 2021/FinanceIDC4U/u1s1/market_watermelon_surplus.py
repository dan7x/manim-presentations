from manimlib import *
from custom.util import get_svg_path, shift_mobject
from custom.tables import AnimatedTable
from custom.gen_util.graphics import LabelledHead
from custom.gen_util.custom_anim import shift_from_current_position

class SurplusBody(Scene):
    def construct(self):
        water_melon_image = get_svg_path("water_melon.png", file=__file__)

        table_dict = self.demand_tables()
        sup_table_dict = self.supply_tables()

        you_head = LabelledHead("You", True).get_head_obj()

        phil_head = LabelledHead("Phillip", False).get_head_obj()
        wendy_head = LabelledHead("Wendy", False, is_boy = False).get_head_obj()
        joe_head = LabelledHead("Joe", False).get_head_obj()
        candice_head = LabelledHead("Candice", False, is_boy = False).get_head_obj()

        heads = [
            you_head,phil_head,wendy_head,joe_head,candice_head
        ]

        for head in heads:
            head.scale(0.4)

        your_tbl_group = VGroup(
            table_dict["you"],
            you_head
        ).arrange(DOWN, buff = 0.3)

        phil_tbl_group = VGroup(
            table_dict["phillip"],
            phil_head
        ).arrange(DOWN, buff = 0.3)
        wendy_tbl_group = VGroup(
            table_dict["wendy"],
            wendy_head
        ).arrange(DOWN, buff = 0.3)
        joe_tbl_group = VGroup(
            table_dict["joe"],
            joe_head
        ).arrange(DOWN, buff = 0.3)
        candice_tbl_group = VGroup(
            table_dict["candice"],
            candice_head
        ).arrange(DOWN, buff = 0.3)

        tables_group_1 = VGroup(
            phil_tbl_group,
            your_tbl_group,
            wendy_tbl_group,
        ).arrange(RIGHT, buff = 0.5)

        tables_group_2 = VGroup(
            joe_tbl_group,
            candice_tbl_group
        ).arrange(RIGHT, buff = 0.5)

        tables_group = VGroup(
            tables_group_1,
            tables_group_2
        ).arrange(DOWN, buff = 0.5)

        t_temp = your_tbl_group.copy().scale(1.5).move_to(ORIGIN)

        a_len = 1
        y_off = 1.45
        a_x_offset = 2.5

        arrow_start = np.add(t_temp.get_center(), [a_x_offset, y_off,0])
        arrow_end = np.add(t_temp.get_center(), [a_x_offset - a_len, y_off,0])

        indexer_arrow = Arrow(arrow_start, arrow_end)

        self.play(ShowCreation(t_temp), run_time=3)

        self.wait(3)

        self.play(ShowCreation(indexer_arrow))

        self.wait(3)

        off_const = 0.35

        self.play(shift_from_current_position(indexer_arrow, [0, -off_const, 0]))
        self.wait(1.5)
        self.play(shift_from_current_position(indexer_arrow, [0, -off_const, 0]))
        self.wait(0.7)
        self.play(shift_from_current_position(indexer_arrow, [0, -off_const, 0]))
        self.wait(0.7)

        self.play(Uncreate(indexer_arrow), Uncreate(t_temp))

        self.wait(1.2)

        self.play(ShowCreation(tables_group), run_time=5)

        mkt_sched_position = [0,0,0]

        self.wait(4)

        for tbl in tables_group:
            for table_obj in tbl:
                tbl_circ = Circle(radius = table_obj.get_width() / 1.5).set_stroke(width=1.7).move_to(table_obj.get_center())

                self.play(ShowCreation(tbl_circ), run_time=0.4)
                self.wait(0.5)
                self.play(Uncreate(tbl_circ), run_time=0.4)

                self.wait(1.5)

        self.wait(6)

        self.play(FadeOutToPoint(phil_tbl_group, mkt_sched_position), run_time=0.4)
        self.play(FadeOutToPoint(your_tbl_group, mkt_sched_position), run_time=0.4)
        self.play(FadeOutToPoint(wendy_tbl_group, mkt_sched_position), run_time=0.4)
        self.play(FadeOutToPoint(joe_tbl_group, mkt_sched_position), run_time=0.4)
        self.play(FadeOutToPoint(candice_tbl_group, mkt_sched_position), run_time=0.4)


        mkt_table = table_dict["market"]

        self.play(
            FadeInFromPoint(mkt_table, mkt_sched_position)
        )

        self.wait(0.5)

        market_shifter = [-3.5, 0, 0]

        self.play(
            shift_from_current_position(mkt_table, market_shifter)
        )

        EQ_QTY = 20
        EQ_P = 4
        DEMAND_YINT = 8

        # GRAPH STUFFS TEST

        sd_axes = Axes(
            x_range = (0, 40, 5),
            y_range = (0, 10),
            height=3,
            width=3,
        ).move_to(-1 * np.array(market_shifter)).scale(1.3)

        sd_axes.add_coordinate_labels(
            font_size=15,
        )

        axes_p = Text("P").scale(0.6).next_to(sd_axes, LEFT)
        axes_q = Text("Q").scale(0.6).next_to(sd_axes, RIGHT)

        shift_mobject(axes_p, [0, sd_axes.get_height()/ 2, 0])
        shift_mobject(axes_q, [0, - sd_axes.get_height()/ 2, 0])

        self.play(ShowCreation(sd_axes),
        ShowCreation(axes_p),
        ShowCreation(axes_q),
        )

        demand_graph = sd_axes.get_graph(
            lambda x : (x - 40) / -5,
            color = RED,
            x_range = (0, 40)
        )

        supply_graph = sd_axes.get_graph(
            lambda x : x / 5,
            color = BLUE,
            x_range = (0, 40)
        )

        bounds_graph = sd_axes.get_graph(
            lambda x : EQ_P
        )

        demand_label = sd_axes.get_graph_label(demand_graph, "D")
        supp_label = sd_axes.get_graph_label(supply_graph, "S")

        area_surplus = sd_axes.get_riemann_rectangles(
            demand_graph,
            bounded=bounds_graph,
            x_range=(0, EQ_QTY),
            dx=0.02,
            input_sample_type="right",stroke_width=0 ,fill_opacity=0.2, colors=("#FF4242", "#FF0022")
        )

        self.play(ShowCreation(demand_graph), ShowCreation(demand_label))

        self.wait(1)

        # END GRAPH STUFFS TEST

        self.play(Uncreate(mkt_table))

        supply_tables_L = VGroup(
            sup_table_dict["loblaws"],
            sup_table_dict["foody"],
            sup_table_dict["nofrills"],
        ).arrange(DOWN, buff = 0.2)
        supply_tables_R = VGroup(
            sup_table_dict["walmart"],
            sup_table_dict["wholefoods"],
        ).arrange(DOWN, buff = 0.2)
        supply_tables = VGroup(supply_tables_L,supply_tables_R).arrange(RIGHT, buff = 0.5).move_to(market_shifter)

        self.play(ShowCreation(supply_tables))

        self.wait(2)

        lob_circle = Circle(radius = supply_tables_L[0].get_width() / 1.5).set_stroke(width=1.7).move_to(supply_tables_L[0].get_center())

        self.play(ShowCreation(lob_circle), run_time=1)
        self.wait(0.5)
        self.play(Uncreate(lob_circle), run_time=1)

        self.wait(1.5)

        for tables_col in supply_tables:
            for table_item in tables_col:
                self.play(FadeOutToPoint(table_item, market_shifter), run_time=0.4)

        mkt_table = sup_table_dict["market"].move_to(market_shifter)

        self.play(
            FadeInFromPoint(mkt_table, market_shifter)
        )

        self.play(ShowCreation(supply_graph), ShowCreation(supp_label))

        self.wait(7)

        eq_circle = Circle(radius = 0.3, color = PURPLE).move_to(
            sd_axes.c2p(EQ_QTY, EQ_P)
        )

        eq_dot = Dot(point = eq_circle.get_center())

        self.play(ShowCreation(eq_circle), ShowCreation(eq_dot), run_time=0.6)
        self.wait(1.3)
        self.play(Uncreate(eq_circle), Uncreate(eq_dot), run_time=0.6)

        self.play(Uncreate(mkt_table))

        indexer = lambda x : (sd_axes.i2gp(0, demand_graph)[x] +  sd_axes.i2gp(EQ_QTY, bounds_graph)[x] + sd_axes.i2gp(EQ_QTY, demand_graph)[x])/3
        surplus_centroid_center = np.array([indexer(0), indexer(1), 0])
        surplus_line_left = np.add(surplus_centroid_center, [1.5, 1, 0])

        arrow_to_surplus = Arrow(surplus_line_left, surplus_centroid_center)
        arrow_to_surplus.set_thickness(0.02)
        surplus_label = Text("Consumer Surplus")
        surplus_label.scale(0.3)
        surplus_label.move_to(np.add(surplus_line_left, [1, 0, 0]))

        v_line_gph = sd_axes.get_v_line_to_graph(EQ_QTY, demand_graph)
        h_line_gph = sd_axes.get_h_line_to_graph(EQ_QTY, demand_graph)

        self.play(ShowCreation(v_line_gph), ShowCreation(h_line_gph))

        dot_gph = Dot(color=RED)
        dot_gph.move_to(sd_axes.i2gp(10, demand_graph))
        self.play(FadeIn(dot_gph, scale=0.5))

        x_tracker = ValueTracker(10)

        f_always(
            dot_gph.move_to,
            lambda: sd_axes.i2gp(x_tracker.get_value(), demand_graph)
        )

        circle_six = Circle(radius = 0.3, color = PURPLE).move_to(
            sd_axes.c2p(10, 6.1)
        )

        self.play(ShowCreation(circle_six), run_time=0.6)
        self.wait(1.3)
        self.play(Uncreate(circle_six), run_time=0.6)

        self.wait(5)

        # the sum of differences

        self.play(x_tracker.animate.set_value(19), run_time=4)
        self.play(x_tracker.animate.set_value(3), run_time=4)

        self.play(Uncreate(dot_gph))

        self.play(ShowCreation(area_surplus))

        EXP_BUFF = 0.15

        original_tri_exp = VGroup(
            Tex("CS"),
            Tex("="),
            Tex("A_{Triangle}")
        ).arrange(RIGHT, buff = EXP_BUFF)

        actual_tri_exp = VGroup(
            Tex("CS"),
            Tex("="),
            Tex("\\frac{1}{2}bh")
        ).arrange(RIGHT, buff = EXP_BUFF)

        actual_tri_calc = VGroup(
            Tex("CS"),
            Tex("="),
            Tex("\\frac{1}{2}(20)(4)")
        ).arrange(RIGHT, buff = EXP_BUFF)

        final_cs = VGroup(
            Tex("CS"),
            Tex("="),
            Tex("\$40.00")
        ).arrange(RIGHT, buff = EXP_BUFF)

        header_csurp = Text("Calculate Consumer Surplus:").scale(0.55)

        cons_surp_container = VGroup(
            header_csurp,
            original_tri_exp,
            actual_tri_exp,
            actual_tri_calc,
            final_cs
        ).arrange(DOWN, buff = 0.3).move_to(market_shifter)

        h_line = Line(sd_axes.c2p(0, EQ_P), sd_axes.c2p(0, DEMAND_YINT))
        shift_mobject(h_line, [-0.3, 0, 0])
        b_line = Line(sd_axes.c2p(0, EQ_P), sd_axes.c2p(EQ_QTY, EQ_P))

        h_brace = Brace(h_line, direction = LEFT)
        b_brace = Brace(b_line, direction = DOWN)

        h_label = Tex("h").next_to(h_brace, LEFT)
        b_label = Tex("b").next_to(b_brace, DOWN)

        self.play(ShowCreation(cons_surp_container[0]))

        self.play(ShowCreation(h_brace), ShowCreation(b_brace))
        self.play(ShowCreation(h_label), ShowCreation(b_label))

        self.wait(1)

        self.play(ShowCreation(cons_surp_container[1]))

        self.wait(1)

        self.play(
            TransformMatchingTex(cons_surp_container[1][0].copy(), cons_surp_container[2][0]),
            TransformMatchingTex(cons_surp_container[1][1].copy(), cons_surp_container[2][1]),
            TransformMatchingTex(cons_surp_container[1][2].copy(), cons_surp_container[2][2])
        )

        self.wait(1)

        self.play(
            TransformMatchingTex(h_label.copy(), cons_surp_container[2][2]),
            TransformMatchingTex(b_label.copy(), cons_surp_container[2][2])
        )

        self.wait(1)

        self.play(
            TransformMatchingTex(cons_surp_container[2][0].copy(), cons_surp_container[3][0]),
            TransformMatchingTex(cons_surp_container[2][1].copy(), cons_surp_container[3][1]),
            TransformMatchingTex(cons_surp_container[2][2].copy(), cons_surp_container[3][2]),
            Uncreate(h_label), Uncreate(h_brace), Uncreate(b_brace), Uncreate(b_label)
        )

        self.wait(1)

        self.play(
            TransformMatchingTex(cons_surp_container[3][0].copy(), cons_surp_container[4][0]),
            TransformMatchingTex(cons_surp_container[3][1].copy(), cons_surp_container[4][1]),
            TransformMatchingTex(cons_surp_container[3][2].copy(), cons_surp_container[4][2])
        )

        self.wait(1)

        self.play(
            FadeOutToPoint(cons_surp_container[1], cons_surp_container[1].get_center()),
            FadeOutToPoint(cons_surp_container[2], cons_surp_container[2].get_center()),
            FadeOutToPoint(cons_surp_container[3], cons_surp_container[3].get_center()),
            shift_from_current_position(cons_surp_container[4],[0, 1.76, 0])
        )

        self.wait(1)

        PAD = 0.06
        final_answ_box = Rectangle(final_cs.get_width()+ 2 * PAD, final_cs.get_height() + 2 * PAD).set_stroke(width=0.75).move_to(final_cs.get_center())

        self.play(ShowCreation(final_answ_box))
        self.wait(0.065)
        self.play(Uncreate(final_answ_box))
        #find all market surplus... one example : originally consume [x] watermelon for [y] dollars
        # animate this motion on chart

        self.wait(2)

        self.play(
            Uncreate(header_csurp),
            Uncreate(final_cs),
            Uncreate(h_line_gph),
            Uncreate(v_line_gph),
            Uncreate(demand_graph), Uncreate(demand_label),
            Uncreate(supply_graph), Uncreate(supp_label),
            Uncreate(area_surplus),
            Uncreate(sd_axes),
            Uncreate(axes_p),
            Uncreate(axes_q),
        )

    def demand_tables(self):

        p_head = "Price"
        d_head = "{{Q_D}}"
        ds_you = [
            [p_head, d_head],
            [6, 1],
            [5, 2],
            [4, 3],
            [3, 4],
            [2, 5],
            [1, 6],
        ]

        ds_phillip = [
            [p_head, d_head],
            [6, 2],
            [5, 3],
            [4, 4],
            [3, 5],
            [2, 6],
            [1, 7],
        ]

        ds_wendy = [
            [p_head, d_head],
            [6, 2],
            [5, 3],
            [4, 4],
            [3, 5],
            [2, 6],
            [1, 7],
        ]

        ds_joe = [
            [p_head, d_head],
            [6, 1],
            [5, 2],
            [4, 3],
            [3, 4],
            [2, 5],
            [1, 6],
        ]

        ds_candice = [
            [p_head, d_head],
            [6, 4],
            [5, 5],
            [4, 6],
            [3, 7],
            [2, 8],
            [1, 9],
        ]

        TITLE_BUFF = 0.25
        C_WIDTH = 0.9
        C_HEIGHT = 0.22
        HEADER_SIZE = 0.5
        BORDER_STROKE = 0.5

        you_table = AnimatedTable(ds_you, table_header = "Your Demand Schedule").get_table_to_draw(C_WIDTH, C_HEIGHT, title_buff = TITLE_BUFF, table_header_size = HEADER_SIZE, border_weight = BORDER_STROKE)
        phil_table =  AnimatedTable(ds_phillip, table_header = "Phillip's Demand Schedule").get_table_to_draw(C_WIDTH, C_HEIGHT, title_buff = TITLE_BUFF, table_header_size = HEADER_SIZE, border_weight = BORDER_STROKE)
        wendy_table = AnimatedTable(ds_wendy, table_header = "Wendy's Demand Schedule").get_table_to_draw(C_WIDTH, C_HEIGHT, title_buff = TITLE_BUFF, table_header_size = HEADER_SIZE, border_weight = BORDER_STROKE)
        joe_table =  AnimatedTable(ds_joe, table_header = "Joe's Demand Schedule").get_table_to_draw(C_WIDTH, C_HEIGHT, title_buff = TITLE_BUFF, table_header_size = HEADER_SIZE, border_weight = BORDER_STROKE)
        candice_table = AnimatedTable(ds_candice, table_header = "Candice's Demand Schedule").get_table_to_draw(C_WIDTH, C_HEIGHT, title_buff = TITLE_BUFF, table_header_size = HEADER_SIZE, border_weight = BORDER_STROKE)

        d_data = [ds_you, ds_phillip, ds_candice, ds_wendy, ds_joe]

        sum_at_price = lambda ind: sum([q[ind][1] for q in d_data])

        mkt_demand_schedule = [
            ["Price", "{{Q_D}}"],
            [6, sum_at_price(1)],
            [5, sum_at_price(2)],
            [4, sum_at_price(3)],
            [3, sum_at_price(4)],
            [2, sum_at_price(5)],
            [1, sum_at_price(6)],
        ]

        mkt_table = AnimatedTable(mkt_demand_schedule, table_header = "Market Demand Schedule", v_padding = 0.25, h_padding = 0.25).get_table_to_draw(2.0, 0.5, title_buff = 0.25, table_header_size = 1.3)

        return {
            "you" : you_table,
            "phillip" : phil_table,
            "wendy" : wendy_table,
            "joe" : joe_table,
            "candice" : candice_table,
            "market" : mkt_table
        }

    def supply_tables(self):
        p_head = "Price"
        d_head = "{{Q_D}}"
        ds_loblaws = [
            [p_head, d_head],
            [6, 6],
            [5, 5],
            [4, 4],
            [3, 3],
            [2, 2],
            [1, 1],
        ]

        ds_walmart = [
            [p_head, d_head],
            [6, 6],
            [5, 5],
            [4, 4],
            [3, 3],
            [2, 2],
            [1, 1],
        ]

        ds_foody = [
            [p_head, d_head],
            [6, 6],
            [5, 5],
            [4, 4],
            [3, 3],
            [2, 2],
            [1, 1],
        ]

        ds_nofrills = [
            [p_head, d_head],
            [6, 6],
            [5, 5],
            [4, 4],
            [3, 3],
            [2, 2],
            [1, 1],
        ]

        ds_wholefoods = [
            [p_head, d_head],
            [6, 6],
            [5, 5],
            [4, 4],
            [3, 3],
            [2, 2],
            [1, 1],
        ]

        TITLE_BUFF = 0.25
        C_WIDTH = 0.9
        C_HEIGHT = 0.22
        HEADER_SIZE = 0.5
        BORDER_STROKE = 0.5

        lob_table = AnimatedTable(ds_loblaws, table_header = "Loblaws").get_table_to_draw(C_WIDTH, C_HEIGHT, title_buff = TITLE_BUFF, table_header_size = HEADER_SIZE, border_weight = BORDER_STROKE)
        foody_table =  AnimatedTable(ds_foody, table_header = "Foody Mart").get_table_to_draw(C_WIDTH, C_HEIGHT, title_buff = TITLE_BUFF, table_header_size = HEADER_SIZE, border_weight = BORDER_STROKE)
        no_frills_tbl = AnimatedTable(ds_nofrills, table_header = "No Frills").get_table_to_draw(C_WIDTH, C_HEIGHT, title_buff = TITLE_BUFF, table_header_size = HEADER_SIZE, border_weight = BORDER_STROKE)
        walmart_table =  AnimatedTable(ds_walmart, table_header = "Walmart").get_table_to_draw(C_WIDTH, C_HEIGHT, title_buff = TITLE_BUFF, table_header_size = HEADER_SIZE, border_weight = BORDER_STROKE)
        whole_foods_tbl = AnimatedTable(ds_wholefoods, table_header = "Whole Foods").get_table_to_draw(C_WIDTH, C_HEIGHT, title_buff = TITLE_BUFF, table_header_size = HEADER_SIZE, border_weight = BORDER_STROKE)

        d_data = [ds_loblaws, ds_foody, ds_nofrills, ds_walmart, ds_wholefoods]

        sum_at_price = lambda ind: sum([q[ind][1] for q in d_data])

        mkt_supply_schedule = [
            ["Price", "{{Q_D}}"],
            [6, sum_at_price(1)],
            [5, sum_at_price(2)],
            [4, sum_at_price(3)],
            [3, sum_at_price(4)],
            [2, sum_at_price(5)],
            [1, sum_at_price(6)],
        ]

        mkt_table = AnimatedTable(mkt_supply_schedule, table_header = "Market Supply Schedule", v_padding = 0.25, h_padding = 0.25).get_table_to_draw(2.0, 0.5, title_buff = 0.25, table_header_size = 1.3)

        return {
            "loblaws" : lob_table,
            "foody" : foody_table,
            "nofrills" : no_frills_tbl,
            "walmart" : walmart_table,
            "wholefoods" : whole_foods_tbl,
            "market": mkt_table
        }
