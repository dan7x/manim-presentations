from manimlib import *

class OpeningScene(Scene):
    def construct(self):
        title_text = [Text("Consumer Surplus"), Text("Consumer Surplus")] # text, text_back
        header_text = Text("IDC4U Summative Assignment 1")
        name_text = Text("By Daniel Xiao")

        header_text.scale(0.25)
        for title_item in title_text:
            title_item.scale(1.5)
        name_text.scale(0.6)

        title_pos_vec = np.array([0, 1.5, 0])
        title_pos_back_vec = np.add(title_pos_vec, [-0.05, 0.05, 0])
        title_text[1].set_color(LIGHT_GRAY)

        title_text[0].move_to(title_pos_vec)
        title_text[1].move_to(title_pos_back_vec)
        header_text.to_edge(TOP, buff=0.05)

        name_text.set_color(LIGHT_GRAY)
        header_text.set_color(LIGHT_GRAY)

        self.play(Write(title_text[1]), Write(title_text[0]), Write(header_text))
        self.wait(0.5)

        opening_graph = self.play_intro_graph()

        name_text_vec = np.array([opening_graph.get_center()[0] + 5, opening_graph.get_center()[1], 0])

        new_graph_pos = np.add(opening_graph.get_center(), [-2, 0, 0])
        self.play(opening_graph.animate.move_to(new_graph_pos), run_time=1)

        name_text.move_to(name_text_vec)
        self.play(Write(name_text))

        self.wait(1)

        self.play(Uncreate(title_text[0]),
            Uncreate(title_text[1]),
            Uncreate(header_text),
            Uncreate(name_text),
            Uncreate(opening_graph))

        self.wait(1.2)

    def play_intro_graph(self):
        AXES_WH = 6 # axes width and height are the same cuz economics
        EQ_QTY = 3
        X_RANGE_UPPER_BOUND = 6
        X_RANGE_LOWER_BOUND = 0
        EQ_PRICE = 4

        axes = Axes((0, 7), (0, 8), height=AXES_WH, width=AXES_WH)
        axes.scale(0.5)
        axes.to_edge(BOTTOM, buff=0.25)

        demand_graph = axes.get_graph(
            lambda x : -x + 7,
            x_range = (X_RANGE_LOWER_BOUND, X_RANGE_UPPER_BOUND),
            color = RED,
            )
        demand_graph_label = axes.get_graph_label(demand_graph, "D")

        supply_graph = axes.get_graph(
            lambda x : x + 1,
            x_range = (X_RANGE_LOWER_BOUND, X_RANGE_UPPER_BOUND),
            color = BLUE,
            )

        bounds_graph = axes.get_graph(
            lambda x : EQ_PRICE,
            x_range=(X_RANGE_LOWER_BOUND, X_RANGE_UPPER_BOUND),
            color = DARK_GRAY
        )

        supply_graph_label = axes.get_graph_label(supply_graph, "S")

        pe_label = Tex("{{P_e}}")
        qe_label = Tex("{{Q_e}}")

        pe_label.scale(0.5)
        qe_label.scale(0.5)

        v_line = axes.get_v_line_to_graph(EQ_QTY, demand_graph)
        h_line = axes.get_h_line_to_graph(EQ_QTY, demand_graph)

        pe_label.next_to(h_line, LEFT)
        qe_target = [v_line.get_center()[0], v_line.get_center()[1] - v_line.get_height() / 2 - 0.35, 0]
        qe_label.move_to(qe_target)

        area_surplus = axes.get_riemann_rectangles(
            demand_graph,
            bounded=bounds_graph,
            x_range=(X_RANGE_LOWER_BOUND, EQ_QTY),
            dx=0.05,
            input_sample_type="right",stroke_width=0,stroke_color=BLACK,fill_opacity=0.3,colors=(RED, RED)
        )

        indexer = lambda x : (axes.i2gp(0, demand_graph)[x] +  axes.i2gp(0, bounds_graph)[x] + axes.i2gp(EQ_QTY, demand_graph)[x])/3
        surplus_centroid_center = np.array([indexer(0), indexer(1), 0])
        surplus_line_left = np.add(surplus_centroid_center, [-1.5, 1, 0])

        arrow_to_surplus = Arrow(surplus_line_left, surplus_centroid_center)
        arrow_to_surplus.set_thickness(0.02)
        surplus_label = Text("Consumer Surplus")
        surplus_label.scale(0.3)
        surplus_label.move_to(np.add(surplus_line_left, [-1, 0, 0]))

        graph_group = VGroup(axes, area_surplus, demand_graph, demand_graph_label, supply_graph,
            supply_graph_label, pe_label, qe_label, v_line, h_line, arrow_to_surplus, surplus_label)

        self.play(
            ShowCreation(area_surplus),
            ShowCreation(demand_graph),
            FadeIn(demand_graph_label, RIGHT),
            ShowCreation(supply_graph),
            FadeIn(supply_graph_label, RIGHT),
            Write(axes, lag_ratio=0.01, run_time=1),
        )

        self.play(
            ShowCreation(pe_label),
            ShowCreation(qe_label),
            ShowCreation(v_line),
            ShowCreation(h_line),
            ShowCreation(surplus_label),
            ShowCreation(arrow_to_surplus),
        )

        return graph_group
