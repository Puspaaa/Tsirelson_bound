"""
Manim animations for Speaker 1: "The Mystery of the Quantum Limit"
Run: manim -qh --format=webm manim_scenes.py <SceneName>
"""

from manim import *
import numpy as np


# ─────────────────────────────────────────────────────────
# Scene 1: Correlation Polytope  →  assets/1_polytope.webm
# ─────────────────────────────────────────────────────────
class CorrelationPolytope(Scene):
    """
    Shows the hierarchy:
      Local (inner square) ⊂ Quantum (circle-ish convex body) ⊂ No-Signaling (outer square)
    The CHSH space is parametrized by two coordinates related to
    correlators. We animate the three nested sets.
    """

    def construct(self):
        self.camera.background_color = "#0f0f1a"

        # --- axes (faint) ---
        axes = Axes(
            x_range=[-0.3, 1.3, 0.5],
            y_range=[-0.3, 1.3, 0.5],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"color": GREY_D, "stroke_width": 1},
        ).shift(LEFT * 0.5)

        # Coordinate labels
        x_label = MathTex(r"\langle A_0 B_0 \rangle", font_size=28, color=GREY_B).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = MathTex(r"\langle A_0 B_1 \rangle", font_size=28, color=GREY_B).next_to(axes.y_axis, LEFT, buff=0.3)

        # ---- No-Signaling square (outer) ----
        ns_vertices = [
            axes.c2p(0, 0),
            axes.c2p(1, 0),
            axes.c2p(1, 1),
            axes.c2p(0, 1),
        ]
        ns_square = Polygon(
            *ns_vertices,
            color="#ff4444",
            fill_color="#ff4444",
            fill_opacity=0.08,
            stroke_width=2.5,
        )
        ns_label = MathTex(r"\mathcal{NS}", font_size=34, color="#ff4444").move_to(
            axes.c2p(0.92, 0.92)
        )

        # ---- Local square (inner, rotated 45°) ----
        # The local polytope in the CHSH slice is a square rotated 45° inside the NS square
        cx, cy = 0.5, 0.5
        r_local = 0.25 * np.sqrt(2)  # half-diagonal
        local_vertices = [
            axes.c2p(cx, cy + r_local),
            axes.c2p(cx + r_local, cy),
            axes.c2p(cx, cy - r_local),
            axes.c2p(cx - r_local, cy),
        ]
        local_square = Polygon(
            *local_vertices,
            color="#44aaff",
            fill_color="#44aaff",
            fill_opacity=0.15,
            stroke_width=2.5,
        )
        local_label = MathTex(r"\mathcal{L}", font_size=34, color="#44aaff").move_to(
            axes.c2p(0.5, 0.5)
        )

        # ---- Quantum set (convex body between L and NS) ----
        # We approximate it as a rounded shape (circle inscribed between the two squares)
        # In the CHSH correlation space, the quantum set is a disk of radius 1/(2√2)
        # centered at (0.5, 0.5) in our coordinates — actually it's more complex,
        # but visually we represent it as a smooth convex body.
        n_pts = 100
        theta = np.linspace(0, 2 * np.pi, n_pts)
        # Use a superellipse to get a shape between circle and square
        quantum_r = 0.42  # tuned for visual
        exp_param = 2.5   # superellipse exponent (2=circle, ∞=square)
        qx = cx + quantum_r * np.sign(np.cos(theta)) * np.abs(np.cos(theta)) ** (2 / exp_param)
        qy = cy + quantum_r * np.sign(np.sin(theta)) * np.abs(np.sin(theta)) ** (2 / exp_param)
        quantum_pts = [axes.c2p(qx[i], qy[i]) for i in range(n_pts)]
        quantum_body = Polygon(
            *quantum_pts,
            color="#aa44ff",
            fill_color="#aa44ff",
            fill_opacity=0.12,
            stroke_width=2.5,
        )
        quantum_label = MathTex(r"\mathcal{Q}", font_size=34, color="#aa44ff").move_to(
            axes.c2p(0.72, 0.72)
        )

        # ---- PR-box dot ----
        pr_dot = Dot(axes.c2p(1, 1), radius=0.08, color=YELLOW)
        pr_label = MathTex(r"\text{PR}", font_size=28, color=YELLOW).next_to(pr_dot, UR, buff=0.12)

        # ---- Legend (right side) ----
        legend_title = Text("Correlation Sets", font_size=22, color=WHITE, weight=BOLD).to_edge(RIGHT).shift(UP * 2.5 + LEFT * 0.3)
        legend_items = VGroup(
            VGroup(Square(side_length=0.2, color="#44aaff", fill_opacity=0.4), Text("Local (L)", font_size=18, color="#44aaff")).arrange(RIGHT, buff=0.15),
            VGroup(Square(side_length=0.2, color="#aa44ff", fill_opacity=0.4), Text("Quantum (Q)", font_size=18, color="#aa44ff")).arrange(RIGHT, buff=0.15),
            VGroup(Square(side_length=0.2, color="#ff4444", fill_opacity=0.4), Text("No-Signaling (NS)", font_size=18, color="#ff4444")).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.06, color=YELLOW), Text("PR-Box", font_size=18, color=YELLOW)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(legend_title, DOWN, aligned_edge=LEFT, buff=0.3)

        # ---- S-value annotation ----
        s_text = VGroup(
            MathTex(r"S \leq 3", font_size=26, color="#44aaff"),
            MathTex(r"S \leq 2+\sqrt{2}", font_size=26, color="#aa44ff"),
            MathTex(r"S \leq 4", font_size=26, color="#ff4444"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT).shift(DOWN * 1.0 + LEFT * 0.3)

        # ============== ANIMATION ==============
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.2)
        self.wait(0.3)

        # 1) Local square appears
        self.play(
            DrawBorderThenFill(local_square),
            Write(local_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # 2) Local expands / morphs into Quantum body
        self.play(
            FadeIn(quantum_body, scale=0.8),
            Write(quantum_label),
            run_time=2,
        )
        self.wait(0.5)

        # 3) No-Signaling square encloses everything
        self.play(
            DrawBorderThenFill(ns_square),
            Write(ns_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # 4) PR-box dot
        self.play(
            FadeIn(pr_dot, scale=2),
            Write(pr_label),
            Flash(pr_dot, color=YELLOW, line_length=0.3, flash_radius=0.4),
            run_time=1.2,
        )
        self.wait(0.5)

        # 5) Legend + S-value annotations
        self.play(
            FadeIn(legend_title, shift=RIGHT * 0.3),
            FadeIn(legend_items, shift=RIGHT * 0.3),
            FadeIn(s_text, shift=RIGHT * 0.3),
            run_time=1.5,
        )

        # 6) Pulse the gap
        gap_arrow = Arrow(
            axes.c2p(0.85, 0.88),
            axes.c2p(0.97, 0.97),
            color=YELLOW,
            stroke_width=3,
            buff=0.05,
            max_tip_length_to_length_ratio=0.2,
        )
        gap_label = Text("The Gap", font_size=20, color=YELLOW, slant=ITALIC).next_to(gap_arrow, LEFT, buff=0.1).shift(DOWN * 0.15)
        self.play(GrowArrow(gap_arrow), FadeIn(gap_label), run_time=1)
        self.play(
            Indicate(gap_arrow, color=YELLOW, scale_factor=1.1),
            run_time=1,
        )

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene 2: PR-Box highlight  →  assets/2_prbox.webm
# ─────────────────────────────────────────────────────────
class PRBoxScene(Scene):
    """
    Shows the PR-Box as a black-box device with two inputs (x,y)
    and two outputs (a,b), along with its defining correlations.
    """

    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("The PR-Box", font_size=40, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        # --- The Box ---
        box = RoundedRectangle(
            corner_radius=0.2,
            width=3.5,
            height=2.5,
            color="#aa44ff",
            fill_color="#1a0a2e",
            fill_opacity=0.9,
            stroke_width=3,
        ).shift(LEFT * 2.5)

        box_label = Text("PR", font_size=36, color="#aa44ff", weight=BOLD).move_to(box.get_center())

        # Inputs
        input_x = Arrow(
            box.get_top() + LEFT * 0.8 + UP * 1.0,
            box.get_top() + LEFT * 0.8,
            color=TEAL,
            stroke_width=3,
            buff=0,
        )
        input_y = Arrow(
            box.get_top() + RIGHT * 0.8 + UP * 1.0,
            box.get_top() + RIGHT * 0.8,
            color=TEAL,
            stroke_width=3,
            buff=0,
        )
        x_label = MathTex("x", font_size=32, color=TEAL).next_to(input_x, UP, buff=0.1)
        y_label = MathTex("y", font_size=32, color=TEAL).next_to(input_y, UP, buff=0.1)
        alice_label = Text("Alice", font_size=20, color=TEAL_B).next_to(x_label, LEFT, buff=0.3)
        bob_label = Text("Bob", font_size=20, color=TEAL_B).next_to(y_label, RIGHT, buff=0.3)

        # Outputs
        output_a = Arrow(
            box.get_bottom() + LEFT * 0.8,
            box.get_bottom() + LEFT * 0.8 + DOWN * 1.0,
            color=ORANGE,
            stroke_width=3,
            buff=0,
        )
        output_b = Arrow(
            box.get_bottom() + RIGHT * 0.8,
            box.get_bottom() + RIGHT * 0.8 + DOWN * 1.0,
            color=ORANGE,
            stroke_width=3,
            buff=0,
        )
        a_label = MathTex("a", font_size=32, color=ORANGE).next_to(output_a, DOWN, buff=0.1)
        b_label = MathTex("b", font_size=32, color=ORANGE).next_to(output_b, DOWN, buff=0.1)

        # --- Correlation table (right side) ---
        table_title = Text("Defining Property", font_size=24, color=WHITE, weight=BOLD).shift(RIGHT * 3 + UP * 1.5)

        correlations = VGroup(
            MathTex(r"p(a = b \mid 00) = 1", font_size=26, color=GREEN),
            MathTex(r"p(a = b \mid 01) = 1", font_size=26, color=GREEN),
            MathTex(r"p(a = b \mid 10) = 1", font_size=26, color=GREEN),
            MathTex(r"p(a \neq b \mid 11) = 1", font_size=26, color="#ff6666"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(RIGHT * 3 + UP * 0.2)

        # Key results
        chsh_line = MathTex(
            r"\Rightarrow \; S = 4", font_size=32, color=YELLOW
        ).shift(RIGHT * 3 + DOWN * 1.2)

        ns_check = VGroup(
            Text("✓  No-Signaling", font_size=22, color=GREEN),
            Text("✗  Violates Tsirelson", font_size=22, color="#ff4444"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).shift(RIGHT * 3 + DOWN * 2.2)

        # ============== ANIMATION ==============
        # Draw the box
        self.play(Create(box), Write(box_label), run_time=1)

        # Inputs
        self.play(
            GrowArrow(input_x), GrowArrow(input_y),
            Write(x_label), Write(y_label),
            FadeIn(alice_label), FadeIn(bob_label),
            run_time=1,
        )

        # Outputs
        self.play(
            GrowArrow(output_a), GrowArrow(output_b),
            Write(a_label), Write(b_label),
            run_time=1,
        )
        self.wait(0.5)

        # Correlations
        self.play(Write(table_title), run_time=0.6)
        for corr in correlations:
            self.play(FadeIn(corr, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(0.3)

        # CHSH score
        self.play(Write(chsh_line), run_time=0.8)
        self.play(
            Circumscribe(chsh_line, color=YELLOW, buff=0.1),
            run_time=1,
        )

        # Check marks
        self.play(FadeIn(ns_check, shift=UP * 0.2), run_time=0.8)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene 3: Random Access Code  →  assets/3_rac.webm
# ─────────────────────────────────────────────────────────
class RandomAccessCode(Scene):
    """
    Schematic of the Random Access Code (van Dam's game).
    Alice has n bits, sends m bits to Bob, Bob guesses a_b.
    """

    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("Random Access Code", font_size=38, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        subtitle = Text("(van Dam's Game)", font_size=22, color=GREY_B).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(subtitle), run_time=1)

        # ---- Alice ----
        alice_box = RoundedRectangle(
            corner_radius=0.15, width=2.5, height=3.5,
            color=TEAL, fill_color="#0a2a2a", fill_opacity=0.9, stroke_width=2.5,
        ).shift(LEFT * 4.5)
        alice_title = Text("Alice", font_size=26, color=TEAL, weight=BOLD).next_to(alice_box, UP, buff=0.15)

        # Alice's bits
        bits_label = MathTex(r"\vec{a} = (a_0, a_1)", font_size=26, color=WHITE).move_to(alice_box.get_center() + UP * 0.7)
        bits_desc = Text("2 random bits", font_size=18, color=GREY_B).move_to(alice_box.get_center() + UP * 0.1)

        # bit visualization
        bit0 = VGroup(
            Square(side_length=0.5, color=TEAL, fill_opacity=0.3, stroke_width=2),
            MathTex("a_0", font_size=22, color=WHITE),
        ).arrange(ORIGIN).move_to(alice_box.get_center() + DOWN * 0.6 + LEFT * 0.4)
        bit1 = VGroup(
            Square(side_length=0.5, color=TEAL, fill_opacity=0.3, stroke_width=2),
            MathTex("a_1", font_size=22, color=WHITE),
        ).arrange(ORIGIN).move_to(alice_box.get_center() + DOWN * 0.6 + RIGHT * 0.4)

        # ---- Channel ----
        channel_arrow = Arrow(
            LEFT * 2.8, RIGHT * 0.2,
            color=ORANGE, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.1,
        ).shift(UP * 0.3)
        channel_label = MathTex(r"\vec{x}", font_size=30, color=ORANGE).next_to(channel_arrow, UP, buff=0.15)
        channel_desc = Text("1 classical bit", font_size=18, color=ORANGE).next_to(channel_arrow, DOWN, buff=0.15)

        # ---- Shared resource (below the channel) ----
        resource_line = DashedLine(
            LEFT * 4.5 + DOWN * 2.5,
            RIGHT * 4.5 + DOWN * 2.5,
            color="#aa44ff",
            stroke_width=2,
            dash_length=0.15,
        )
        resource_label = Text("Shared Resource (e.g., PR-Box / Entanglement)", font_size=18, color="#aa44ff").next_to(resource_line, DOWN, buff=0.15)

        # ---- Bob ----
        bob_box = RoundedRectangle(
            corner_radius=0.15, width=2.5, height=3.5,
            color="#44aaff", fill_color="#0a1a2e", fill_opacity=0.9, stroke_width=2.5,
        ).shift(RIGHT * 4.5)
        bob_title = Text("Bob", font_size=26, color="#44aaff", weight=BOLD).next_to(bob_box, UP, buff=0.15)

        # Bob's input
        b_label = MathTex(r"b \in \{0, 1\}", font_size=24, color=WHITE).move_to(bob_box.get_center() + UP * 0.9)
        b_desc = Text("choice bit", font_size=18, color=GREY_B).move_to(bob_box.get_center() + UP * 0.35)

        # Bob's guess
        beta_label = MathTex(r"\beta = \text{guess of } a_b", font_size=22, color=YELLOW).move_to(bob_box.get_center() + DOWN * 0.3)

        # Success metric
        success = MathTex(
            r"\eta = P(\beta = a_b)", font_size=24, color=GREEN
        ).move_to(bob_box.get_center() + DOWN * 1.0)

        # ---- Question at bottom ----
        question = Text(
            "How well can Bob guess?  Depends on the shared resource!",
            font_size=22, color=YELLOW, weight=BOLD,
        ).to_edge(DOWN, buff=0.4)

        # ============== ANIMATION ==============
        # Alice appears
        self.play(Create(alice_box), Write(alice_title), run_time=0.8)
        self.play(
            Write(bits_label), FadeIn(bits_desc),
            FadeIn(bit0), FadeIn(bit1),
            run_time=1,
        )
        self.wait(0.3)

        # Channel
        self.play(
            GrowArrow(channel_arrow),
            Write(channel_label), FadeIn(channel_desc),
            run_time=1,
        )
        self.wait(0.3)

        # Bob appears
        self.play(Create(bob_box), Write(bob_title), run_time=0.8)
        self.play(
            Write(b_label), FadeIn(b_desc),
            Write(beta_label),
            Write(success),
            run_time=1.5,
        )
        self.wait(0.3)

        # Shared resource
        self.play(
            Create(resource_line),
            FadeIn(resource_label, shift=UP * 0.2),
            run_time=1,
        )
        self.wait(0.3)

        # Question
        self.play(FadeIn(question, shift=UP * 0.3), run_time=0.8)
        self.play(Indicate(question, color=YELLOW, scale_factor=1.02), run_time=0.8)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene 4: CHSH bar chart  →  assets/4_chsh_bars.webm
# ─────────────────────────────────────────────────────────
class CHSHBars(Scene):
    """
    Animated bar chart comparing CHSH S-values for
    Local, Quantum, and No-Signaling (PR-Box).
    """

    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("CHSH Score Comparison", font_size=36, color=WHITE, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        # values
        labels = ["Classical\n(Local)", "Quantum\n(Tsirelson)", "PR-Box\n(No-Signal.)"]
        values = [3.0, 2 + np.sqrt(2), 4.0]
        colors = ["#44aaff", "#aa44ff", "#ff4444"]
        value_strs = [r"S=3", r"S=2+\sqrt{2}\approx 3.41", r"S=4"]

        bar_width = 1.2
        spacing = 2.0
        max_h = 4.0
        base_y = -1.5

        bars = VGroup()
        bar_labels = VGroup()
        bar_values = VGroup()

        for i, (lbl, val, col, vs) in enumerate(zip(labels, values, colors, value_strs)):
            x = (i - 1) * spacing
            h = (val / 4.0) * max_h

            bar = Rectangle(
                width=bar_width, height=h,
                color=col, fill_color=col, fill_opacity=0.6,
                stroke_width=2,
            ).move_to([x, base_y + h / 2, 0])

            label = Text(lbl, font_size=18, color=col).next_to(bar, DOWN, buff=0.2)
            value_tex = MathTex(vs, font_size=22, color=WHITE).next_to(bar, UP, buff=0.15)

            bars.add(bar)
            bar_labels.add(label)
            bar_values.add(value_tex)

        # Baseline
        baseline = Line(
            LEFT * 3, RIGHT * 3, color=GREY, stroke_width=1
        ).move_to([0, base_y, 0])

        # Tsirelson bound line
        tsirelson_y = base_y + ((2 + np.sqrt(2)) / 4.0) * max_h
        tsirelson_line = DashedLine(
            LEFT * 3.5 + UP * tsirelson_y,
            RIGHT * 3.5 + UP * tsirelson_y,
            color=YELLOW, stroke_width=2, dash_length=0.15,
        ).move_to([0, tsirelson_y, 0])
        tsirelson_label = Text(
            "Tsirelson's Bound", font_size=18, color=YELLOW
        ).next_to(tsirelson_line, RIGHT, buff=0.15)

        # ============== ANIMATION ==============
        self.play(Create(baseline), run_time=0.5)

        # Grow bars one by one
        for i in range(3):
            bar_copy = bars[i].copy().stretch(0.01, dim=1, about_edge=DOWN)
            self.play(
                Transform(bar_copy, bars[i]),
                Write(bar_labels[i]),
                run_time=0.8,
            )
            self.play(Write(bar_values[i]), run_time=0.5)
            self.remove(bar_copy)
            self.add(bars[i])

        self.wait(0.3)

        # Tsirelson bound line
        self.play(
            Create(tsirelson_line),
            Write(tsirelson_label),
            run_time=1,
        )
        self.play(
            Indicate(tsirelson_line, color=YELLOW, scale_factor=1.02),
            run_time=0.8,
        )

        # Question mark above PR-Box bar
        q_mark = Text("?", font_size=60, color=YELLOW, weight=BOLD).next_to(bars[2], UP, buff=0.6)
        self.play(FadeIn(q_mark, scale=2), run_time=0.8)
        self.play(
            q_mark.animate.scale(1.2),
            rate_func=there_and_back,
            run_time=0.8,
        )

        self.wait(2)
