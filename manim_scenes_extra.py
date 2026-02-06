"""
Manim animations for Speaker 1 — additional slides from LaTeX content.
Run: manim -qh --format=webm manim_scenes_extra.py <SceneName>
"""

from manim import *
import numpy as np


# ─────────────────────────────────────────────────────────
# Scene: DPI Visualization  →  assets/5_dpi.webm
# ─────────────────────────────────────────────────────────
class DPIScene(Scene):
    """
    Visualises the Data Processing Inequality:
    Alice & Bob share state P_AB.  Bob applies local operation T.
    Correlations (measured by conditional entropy) cannot increase.
    """

    def construct(self):
        self.camera.background_color = "#0f0f1a"

        # ── Shared state (cloud-like ellipse) ──
        cloud = Ellipse(width=4.5, height=2.0, color="#aa44ff",
                        fill_color="#aa44ff", fill_opacity=0.12,
                        stroke_width=2.5).shift(UP * 2.2)
        cloud_label = MathTex(r"\vec{P}_{AB}", font_size=34,
                              color="#aa44ff").move_to(cloud.get_center())
        cloud_sub = Text("Shared State", font_size=18,
                         color="#aa44ff").next_to(cloud, UP, buff=0.15)

        # ── Alice ──
        alice_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=1.4,
                                     color=TEAL, fill_color="#0a2a2a",
                                     fill_opacity=0.9, stroke_width=2.5).shift(LEFT * 3.5)
        alice_lbl = Text("Alice (A)", font_size=22, color=TEAL,
                         weight=BOLD).move_to(alice_box.get_center())

        # ── Bob ──
        bob_box = RoundedRectangle(corner_radius=0.15, width=2.4, height=1.4,
                                   color="#44aaff", fill_color="#0a1a2e",
                                   fill_opacity=0.9, stroke_width=2.5).shift(RIGHT * 3.5)
        bob_lbl = Text("Bob (B)", font_size=22, color="#44aaff",
                       weight=BOLD).move_to(bob_box.get_center())

        # Connections cloud → Alice/Bob
        dash_a = DashedLine(cloud.get_left() + DOWN * 0.3, alice_box.get_top(),
                            color="#aa44ff", stroke_width=2, dash_length=0.12)
        dash_b = DashedLine(cloud.get_right() + DOWN * 0.3, bob_box.get_top(),
                            color="#aa44ff", stroke_width=2, dash_length=0.12)

        # ── Local operation T ──
        op_box = RoundedRectangle(corner_radius=0.1, width=2.2, height=1.0,
                                  color="#ff9800", fill_color="#2e1a0a",
                                  fill_opacity=0.9, stroke_width=2.5).next_to(bob_box, DOWN, buff=0.7)
        op_lbl = MathTex(r"\text{Operation } T", font_size=24,
                         color="#ff9800").move_to(op_box.get_center())
        op_arrow = Arrow(bob_box.get_bottom(), op_box.get_top(),
                         color="#ff9800", stroke_width=3, buff=0.05,
                         max_tip_length_to_length_ratio=0.2)

        # ── Correlation arrow (decreasing) ──
        corr_arrow = Arrow(RIGHT * 5.8 + UP * 0.5, RIGHT * 5.8 + DOWN * 1.8,
                           color="#ff4444", stroke_width=5, buff=0,
                           max_tip_length_to_length_ratio=0.15)
        corr_label = Text("Correlation", font_size=18, color="#ff4444"
                          ).rotate(PI / 2).next_to(corr_arrow, LEFT, buff=0.15)
        corr_note = Text("Cannot\nIncrease", font_size=16, color="#ff4444",
                         weight=BOLD).next_to(corr_arrow, RIGHT, buff=0.15)

        # ── DPI equation ──
        dpi_eq = MathTex(
            r"H(A|B)_{\vec{P}_{AB}}",
            r"\;\leq\;",
            r"H(A|B')_{(\mathbb{1}\otimes T)\vec{P}_{AB}}",
            font_size=30, color=WHITE
        ).to_edge(DOWN, buff=0.6)
        dpi_eq[0].set_color(TEAL)
        dpi_eq[2].set_color("#ff9800")

        dpi_title = Text("Data Processing Inequality", font_size=20,
                         color=YELLOW, weight=BOLD).next_to(dpi_eq, UP, buff=0.25)

        # ============== ANIMATION ==============
        self.play(Create(cloud), Write(cloud_label), FadeIn(cloud_sub), run_time=1)
        self.play(
            Create(alice_box), Write(alice_lbl),
            Create(bob_box), Write(bob_lbl),
            Create(dash_a), Create(dash_b),
            run_time=1.2
        )
        self.wait(0.3)

        # Local operation
        self.play(GrowArrow(op_arrow), Create(op_box), Write(op_lbl), run_time=1)
        self.wait(0.3)

        # Correlation arrow
        self.play(
            GrowArrow(corr_arrow),
            FadeIn(corr_label), FadeIn(corr_note),
            run_time=1
        )
        self.wait(0.3)

        # DPI equation
        self.play(Write(dpi_title), run_time=0.6)
        self.play(Write(dpi_eq), run_time=1.5)
        self.play(Circumscribe(dpi_eq, color=YELLOW, buff=0.12), run_time=1)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene: GPT Framework  →  assets/6_gpt.webm
# ─────────────────────────────────────────────────────────
class GPTScene(Scene):
    """
    Shows the shift from Hilbert-space QM to operational/probabilistic view.
    Left: Traditional QM (wavefunction, crossed out).
    Right: Operational view (probability bars).
    """

    def construct(self):
        self.camera.background_color = "#0f0f1a"

        divider = DashedLine(UP * 3, DOWN * 3, color=GREY_D,
                             stroke_width=1.5, dash_length=0.15)

        # ─── LEFT: Traditional QM ───
        left_title = Text("Traditional QM", font_size=24, color=GREY,
                          weight=BOLD).move_to(LEFT * 3.5 + UP * 2.5)

        # Wavefunction plot
        wave_axes = Axes(x_range=[0, 4, 1], y_range=[-1, 1, 0.5],
                         x_length=4, y_length=2, tips=False,
                         axis_config={"color": GREY_D, "stroke_width": 1}
                         ).shift(LEFT * 3.5 + UP * 0.5)
        wave = wave_axes.plot(
            lambda x: 0.7 * np.sin(5 * x) * np.exp(-((x - 2) ** 2) / 1.5),
            color=GREY_B, stroke_width=2
        )
        psi_label = MathTex(r"\psi \in \mathcal{H}", font_size=28,
                            color=GREY).next_to(wave_axes, DOWN, buff=0.3)
        hilbert_label = Text("Hilbert Spaces", font_size=18,
                             color=GREY).next_to(psi_label, DOWN, buff=0.15)

        # Big red X
        cross1 = Line(LEFT * 3.5 + UP * 2 + LEFT * 1.8,
                      LEFT * 3.5 + DOWN * 1.5 + RIGHT * 1.8,
                      color="#ff4444", stroke_width=6, stroke_opacity=0.7)
        cross2 = Line(LEFT * 3.5 + UP * 2 + RIGHT * 1.8,
                      LEFT * 3.5 + DOWN * 1.5 + LEFT * 1.8,
                      color="#ff4444", stroke_width=6, stroke_opacity=0.7)

        # ─── RIGHT: Operational View ───
        right_title = Text("Operational View", font_size=24, color="#44aaff",
                           weight=BOLD).move_to(RIGHT * 3.5 + UP * 2.5)

        # Probability bars
        bar_axes = Axes(x_range=[0, 5, 1], y_range=[0, 1.2, 0.5],
                        x_length=4.5, y_length=2.5, tips=True,
                        axis_config={"color": "#44aaff", "stroke_width": 1.5}
                        ).shift(RIGHT * 3.5 + UP * 0.3)

        bars = VGroup()
        heights = [0.8, 0.35, 0.65, 0.2]
        bar_labels_list = [r"P(0|0)", r"P(1|0)", r"P(0|1)", r"P(1|1)"]
        for i, (h, bl) in enumerate(zip(heights, bar_labels_list)):
            x_pos = 0.7 + i * 1.1
            bar = Rectangle(width=0.7, height=h * 2, color="#00ccff",
                            fill_color="#00ccff", fill_opacity=0.4,
                            stroke_width=2)
            bar.move_to(bar_axes.c2p(x_pos + 0.35, h / 2 * 2 / 2.5 * 1.2))
            bar.stretch_to_fit_height(h * 2)
            bar.move_to([bar_axes.c2p(x_pos + 0.35, 0)[0],
                         bar_axes.c2p(0, 0)[1] + h * 2 / 2, 0])
            bars.add(bar)

        state_label = MathTex(r"\text{State } \vec{P}", font_size=26,
                              color="#44aaff").next_to(bar_axes, UP, buff=0.15)

        # State definition
        state_def = MathTex(
            r"\vec{P} = \big( P(i|j) \big)_{i,j}",
            font_size=26, color=WHITE
        ).to_edge(DOWN, buff=0.8).shift(LEFT * 0.5)
        state_desc = Text("Outcome i given fiducial measurement j",
                          font_size=16, color=GREY_B
                          ).next_to(state_def, DOWN, buff=0.15)

        # Convexity note
        convex = VGroup(
            Text("Convexity:", font_size=18, color="#55ff99", weight=BOLD),
            Text("  Mixtures of states are valid states", font_size=16, color=GREY_B),
        ).arrange(RIGHT, buff=0.15).next_to(state_desc, DOWN, buff=0.25)

        # ============== ANIMATION ==============
        # Left side
        self.play(Write(left_title), run_time=0.6)
        self.play(Create(wave_axes), Create(wave), run_time=1)
        self.play(Write(psi_label), FadeIn(hilbert_label), run_time=0.8)
        self.wait(0.3)

        # Cross it out
        self.play(Create(cross1), Create(cross2), run_time=0.8)
        self.wait(0.3)

        # Divider
        self.play(Create(divider), run_time=0.5)

        # Right side
        self.play(Write(right_title), run_time=0.6)
        self.play(Create(bar_axes), Write(state_label), run_time=0.8)
        for bar in bars:
            self.play(GrowFromEdge(bar, DOWN), run_time=0.3)
        self.wait(0.3)

        # State definition
        self.play(Write(state_def), FadeIn(state_desc), run_time=1)
        self.play(FadeIn(convex, shift=UP * 0.2), run_time=0.8)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene: Systems of Type (k,l)  →  assets/7_systems.webm
# ─────────────────────────────────────────────────────────
class SystemsScene(Scene):
    """
    Compares Quantum (Bloch sphere) vs Box-World (square state space).
    """

    def construct(self):
        self.camera.background_color = "#0f0f1a"

        divider = DashedLine(UP * 2.5, DOWN * 2.5, color=GREY_D,
                             stroke_width=1.5, dash_length=0.15)

        # ─── LEFT: Quantum (Bloch Sphere) ───
        q_title = Text("Quantum", font_size=28, color="#44aaff",
                       weight=BOLD).move_to(LEFT * 3.5 + UP * 2.8)

        # Sphere
        sphere = Circle(radius=1.5, color="#44aaff", fill_color="#00ccff",
                        fill_opacity=0.08, stroke_width=2.5
                        ).shift(LEFT * 3.5 + UP * 0.3)
        # Equator ellipse
        equator = Ellipse(width=3.0, height=0.8, color="#44aaff",
                          stroke_width=1.5, stroke_opacity=0.5
                          ).shift(LEFT * 3.5 + UP * 0.3)
        # "Poles"
        north = Dot(LEFT * 3.5 + UP * 1.8, radius=0.06, color="#44aaff")
        south = Dot(LEFT * 3.5 + DOWN * 1.2, radius=0.06, color="#44aaff")
        axis_line = DashedLine(north.get_center(), south.get_center(),
                               color="#44aaff", stroke_width=1,
                               dash_length=0.1, stroke_opacity=0.4)

        q_desc = Text("Continuous Measurements", font_size=16, color=GREY_B
                      ).move_to(LEFT * 3.5 + DOWN * 2.0)
        q_k = MathTex(r"k \approx d^2", font_size=24, color="#44aaff"
                      ).next_to(q_desc, DOWN, buff=0.15)

        # ─── RIGHT: Box-World ───
        b_title = Text("Box-World", font_size=28, color="#ff9800",
                       weight=BOLD).move_to(RIGHT * 3.5 + UP * 2.8)

        # Square state space
        box_sq = Square(side_length=2.8, color="#ff9800", fill_color="#ff9800",
                        fill_opacity=0.08, stroke_width=2.5
                        ).shift(RIGHT * 3.5 + UP * 0.3)

        # Axes inside
        bx_axis = Arrow(RIGHT * 2.0 + DOWN * 0.9, RIGHT * 5.0 + DOWN * 0.9,
                        color="#ff9800", stroke_width=2, buff=0,
                        max_tip_length_to_length_ratio=0.1)
        by_axis = Arrow(RIGHT * 2.1 + DOWN * 1.0, RIGHT * 2.1 + UP * 1.7,
                        color="#ff9800", stroke_width=2, buff=0,
                        max_tip_length_to_length_ratio=0.1)

        # Corner dots (extremal states)
        corners = VGroup(*[
            Dot(box_sq.get_corner(d), radius=0.06, color=YELLOW)
            for d in [UL, UR, DL, DR]
        ])

        b_desc = Text("System Type (2, 2)", font_size=16, color=GREY_B
                      ).move_to(RIGHT * 3.5 + DOWN * 2.0)
        b_k = MathTex(r"k=2 \text{ fiducial meas.}", font_size=22,
                      color="#ff9800").next_to(b_desc, DOWN, buff=0.15)

        # ─── Bottom summary ───
        summary = VGroup(
            MathTex(r"\text{System of type } (k, l):", font_size=26, color=WHITE),
            MathTex(r"k \text{ measurements, } l \text{ outcomes each}",
                    font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.4)

        # ============== ANIMATION ==============
        # Quantum side
        self.play(Write(q_title), run_time=0.6)
        self.play(
            Create(sphere), Create(equator),
            Create(axis_line), FadeIn(north), FadeIn(south),
            run_time=1.2
        )
        self.play(FadeIn(q_desc), Write(q_k), run_time=0.8)

        self.play(Create(divider), run_time=0.5)

        # Box-World side
        self.play(Write(b_title), run_time=0.6)
        self.play(
            Create(box_sq), GrowArrow(bx_axis), GrowArrow(by_axis),
            FadeIn(corners),
            run_time=1.2
        )
        self.play(FadeIn(b_desc), Write(b_k), run_time=0.8)

        # Summary
        self.play(FadeIn(summary, shift=UP * 0.3), run_time=1)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene: Composite Systems  →  assets/8_composite.webm
# ─────────────────────────────────────────────────────────
class CompositeScene(Scene):
    """
    Composite systems V_AB = V_A ⊗ V_B and the No-Signaling principle.
    Alice's box, Bob's box, barrier between them.
    """

    def construct(self):
        self.camera.background_color = "#0f0f1a"

        # ── Alice ──
        alice_box = RoundedRectangle(corner_radius=0.15, width=3.0, height=2.2,
                                     color=TEAL, fill_color="#0a2a2a",
                                     fill_opacity=0.9, stroke_width=2.5
                                     ).shift(LEFT * 3.5)
        alice_title = Text("Alice", font_size=24, color=TEAL,
                           weight=BOLD).next_to(alice_box, UP, buff=0.15)

        # Switch icon
        switch_a = VGroup(
            Rectangle(width=0.5, height=0.7, color=TEAL, fill_opacity=0.3, stroke_width=2),
            Text("x", font_size=18, color=TEAL),
        ).arrange(ORIGIN).move_to(alice_box.get_center() + UP * 0.3)
        input_a_label = Text("Input x", font_size=16, color=GREY_B
                             ).next_to(switch_a, DOWN, buff=0.2)

        # ── Bob ──
        bob_box = RoundedRectangle(corner_radius=0.15, width=3.0, height=2.2,
                                   color="#44aaff", fill_color="#0a1a2e",
                                   fill_opacity=0.9, stroke_width=2.5
                                   ).shift(RIGHT * 3.5)
        bob_title = Text("Bob", font_size=24, color="#44aaff",
                         weight=BOLD).next_to(bob_box, UP, buff=0.15)

        # P(b|y) const label
        bob_inner = MathTex(r"P(b|y) = \text{const.}", font_size=20,
                            color="#44aaff").move_to(bob_box.get_center())

        # ── No-Signaling barrier ──
        barrier = Line(UP * 1.8, DOWN * 1.8, color="#ff4444",
                       stroke_width=4).shift(RIGHT * 0)
        cross_mark = MathTex(r"\times", font_size=40, color="#ff4444"
                             ).next_to(barrier, UP, buff=0.1)
        ns_label = Text("No-Signaling", font_size=18, color="#ff4444",
                        weight=BOLD).next_to(cross_mark, UP, buff=0.1)

        # Arrow between
        gray_arrow = Arrow(LEFT * 1.8, RIGHT * 1.2, color=GREY_D,
                           stroke_width=3, buff=0,
                           max_tip_length_to_length_ratio=0.12)

        # ── Equations (bottom) ──
        eq_tensor = MathTex(
            r"V_{AB} = V_A \otimes V_B",
            font_size=28, color=WHITE
        ).shift(DOWN * 2.2 + LEFT * 2.5)

        eq_marginal = MathTex(
            r"P_A(i|j) = \sum_{i'} P_{AB}(ii'|jj')",
            font_size=24, color=GREY_B
        ).next_to(eq_tensor, DOWN, buff=0.2)

        # Key point
        key_box = RoundedRectangle(corner_radius=0.1, width=8.5, height=0.9,
                                   color=YELLOW, fill_color="#2e2a0a",
                                   fill_opacity=0.5, stroke_width=2
                                   ).to_edge(DOWN, buff=0.3)
        key_text = Text(
            "Box-world satisfies all these rules... yet violates Tsirelson's bound!",
            font_size=18, color=YELLOW, weight=BOLD
        ).move_to(key_box.get_center())

        # ============== ANIMATION ==============
        self.play(
            Create(alice_box), Write(alice_title),
            Create(bob_box), Write(bob_title),
            run_time=1
        )
        self.play(
            FadeIn(switch_a), FadeIn(input_a_label),
            Write(bob_inner),
            run_time=0.8
        )
        self.wait(0.3)

        # No-signaling barrier
        self.play(
            GrowArrow(gray_arrow), run_time=0.5
        )
        self.play(
            Create(barrier), Write(cross_mark), Write(ns_label),
            run_time=1
        )
        self.wait(0.3)

        # Equations
        self.play(Write(eq_tensor), run_time=0.8)
        self.play(Write(eq_marginal), run_time=0.8)
        self.wait(0.3)

        # Key point
        self.play(
            Create(key_box), Write(key_text),
            run_time=1
        )
        self.play(
            Indicate(key_box, color=YELLOW, scale_factor=1.02),
            run_time=0.8
        )

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Updated CHSH bars with S ≤ 2 convention
#   →  assets/4_chsh_bars.webm
# ─────────────────────────────────────────────────────────
class CHSHBarsV2(Scene):
    """
    Bar chart with standard CHSH convention:
    Classical S ≤ 2, Quantum S ≤ 2√2, No-Signaling S ≤ 4.
    """

    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("CHSH Score Comparison", font_size=36, color=WHITE,
                     weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)

        labels = ["Classical\n(Local)", "Quantum\n(Tsirelson)", "PR-Box\n(No-Signal.)"]
        values = [2.0, 2 * np.sqrt(2), 4.0]
        colors = ["#44aaff", "#aa44ff", "#ff4444"]
        value_strs = [r"S \leq 2", r"S \leq 2\sqrt{2} \approx 2.83", r"S = 4"]

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

            bar = Rectangle(width=bar_width, height=h, color=col,
                            fill_color=col, fill_opacity=0.6, stroke_width=2
                            ).move_to([x, base_y + h / 2, 0])

            label = Text(lbl, font_size=18, color=col).next_to(bar, DOWN, buff=0.2)
            value_tex = MathTex(vs, font_size=22, color=WHITE).next_to(bar, UP, buff=0.15)

            bars.add(bar)
            bar_labels.add(label)
            bar_values.add(value_tex)

        baseline = Line(LEFT * 3, RIGHT * 3, color=GREY, stroke_width=1
                        ).move_to([0, base_y, 0])

        tsirelson_y = base_y + (2 * np.sqrt(2) / 4.0) * max_h
        tsirelson_line = DashedLine(LEFT * 3.5, RIGHT * 3.5,
                                    color=YELLOW, stroke_width=2,
                                    dash_length=0.15).move_to([0, tsirelson_y, 0])
        tsirelson_label = Text("Tsirelson's Bound", font_size=18, color=YELLOW
                               ).next_to(tsirelson_line, RIGHT, buff=0.15)

        # ============== ANIMATION ==============
        self.play(Create(baseline), run_time=0.5)

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

        self.play(Create(tsirelson_line), Write(tsirelson_label), run_time=1)
        self.play(Indicate(tsirelson_line, color=YELLOW, scale_factor=1.02),
                  run_time=0.8)

        q_mark = Text("?", font_size=60, color=YELLOW, weight=BOLD
                       ).next_to(bars[2], UP, buff=0.6)
        self.play(FadeIn(q_mark, scale=2), run_time=0.8)
        self.play(q_mark.animate.scale(1.2), rate_func=there_and_back, run_time=0.8)

        self.wait(2)
