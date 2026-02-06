"""
Manim animations for Speaker 2: "The Crime & The Law"
Themes: Tsirelson's Bound, PR-Box violation, Information Causality, DPI → IC → Tsirelson chain.

Run all:
  manim -qh --format=webm -o <name>.webm manim_speaker2.py <SceneName>
"""

from manim import *
import numpy as np


# ─────────────────────────────────────────────────────────
# Scene 1: Tsirelson Gauge   →  assets/s2_tsirelson_gauge.webm
# An animated "speedometer" gauge that sweeps from 0→4,
# marking Classical(2), Tsirelson(2√2), and NS(4) regions.
# ─────────────────────────────────────────────────────────
class TsirelsonGauge(Scene):
    def construct(self):
        self.camera.background_color = "#0f0f1a"

        # ── Gauge arc ──
        center = DOWN * 0.3
        radius = 3.2
        start_angle = 150 * DEGREES
        end_angle = 30 * DEGREES
        arc_span = start_angle - end_angle  # 120°

        def s_to_angle(s):
            """Map S ∈ [0, 4] to angle on the gauge."""
            return start_angle - (s / 4.0) * arc_span

        # Background arc (full)
        bg_arc = Arc(radius=radius, start_angle=end_angle, angle=arc_span,
                     color=GREY_D, stroke_width=14, arc_center=center)

        # Classical zone: 0 → 2 (blue)
        classical_arc = Arc(radius=radius, start_angle=s_to_angle(0),
                            angle=-(2/4)*arc_span,
                            color="#44aaff", stroke_width=16,
                            stroke_opacity=0.6, arc_center=center)

        # Quantum zone: 2 → 2√2 (purple)
        q_start = s_to_angle(2)
        q_span = -((2*np.sqrt(2) - 2) / 4) * arc_span
        quantum_arc = Arc(radius=radius, start_angle=q_start, angle=q_span,
                          color="#aa44ff", stroke_width=16,
                          stroke_opacity=0.6, arc_center=center)

        # Forbidden zone: 2√2 → 4 (red, dimmer)
        f_start = s_to_angle(2 * np.sqrt(2))
        f_span = -((4 - 2*np.sqrt(2)) / 4) * arc_span
        forbidden_arc = Arc(radius=radius, start_angle=f_start, angle=f_span,
                            color="#ff4444", stroke_width=16,
                            stroke_opacity=0.3, arc_center=center)

        # ── Tick marks and labels ──
        ticks = VGroup()
        tick_data = [
            (0, "0", GREY_B),
            (2, "2", "#44aaff"),
            (2*np.sqrt(2), r"2\sqrt{2}", "#aa44ff"),
            (4, "4", "#ff4444"),
        ]
        for s_val, label_str, col in tick_data:
            angle = s_to_angle(s_val)
            inner = center + (radius - 0.35) * np.array([np.cos(angle), np.sin(angle), 0])
            outer = center + (radius + 0.35) * np.array([np.cos(angle), np.sin(angle), 0])
            tick = Line(inner, outer, color=col, stroke_width=3)
            label_pos = center + (radius + 0.75) * np.array([np.cos(angle), np.sin(angle), 0])
            label = MathTex(label_str, font_size=26, color=col).move_to(label_pos)
            ticks.add(tick, label)

        # Zone labels (inside arc)
        classical_lbl = Text("Classical", font_size=20, color="#44aaff",
                             weight=BOLD).move_to(center + UP * 1.0 + LEFT * 1.8)
        quantum_lbl = Text("Quantum", font_size=20, color="#aa44ff",
                           weight=BOLD).move_to(center + UP * 2.0)
        forbidden_lbl = Text("Forbidden?", font_size=20, color="#ff4444",
                             weight=BOLD).move_to(center + UP * 1.0 + RIGHT * 1.8)

        # ── Needle (animated) ──
        needle_len = radius - 0.6
        needle = Line(center, center + needle_len * UP, color=WHITE,
                      stroke_width=4)
        needle_dot = Dot(center, radius=0.12, color=WHITE, z_index=5)

        def get_needle(s_val):
            angle = s_to_angle(s_val)
            end = center + needle_len * np.array([np.cos(angle), np.sin(angle), 0])
            return Line(center, end, color=WHITE, stroke_width=4)

        # S-value display
        s_display = MathTex(r"S = 0.00", font_size=40, color=WHITE
                            ).next_to(center, DOWN, buff=0.8)

        # Title
        title = Text("CHSH Score S", font_size=36, color=WHITE,
                     weight=BOLD).to_edge(UP, buff=0.4)

        # ── Side annotations ──
        bounds_text = VGroup(
            MathTex(r"\text{Classical: } S \leq 2", font_size=24, color="#44aaff"),
            MathTex(r"\text{Tsirelson: } S \leq 2\sqrt{2}", font_size=24, color="#aa44ff"),
            MathTex(r"\text{No-Signaling: } S \leq 4", font_size=24, color="#ff4444"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)

        tsirelson_def = MathTex(
            r"2 - \sqrt{2} \;\leq\; S \;\leq\; 2 + \sqrt{2}",
            font_size=28, color="#aa44ff"
        ).to_edge(DOWN, buff=0.4)

        # ============== ANIMATION ==============
        self.play(Write(title), run_time=0.7)
        self.play(Create(bg_arc), run_time=0.8)

        # Draw zone arcs
        self.play(Create(classical_arc), FadeIn(classical_lbl), run_time=1)
        self.play(Create(quantum_arc), FadeIn(quantum_lbl), run_time=1)
        self.play(Create(forbidden_arc), FadeIn(forbidden_lbl), run_time=1)
        self.play(FadeIn(ticks), run_time=0.8)

        # Needle starts at 0
        init_needle = get_needle(0)
        self.play(Create(init_needle), FadeIn(needle_dot), run_time=0.5)
        self.play(FadeIn(s_display), run_time=0.4)

        # Sweep needle to Classical limit (S=2)
        n2 = get_needle(2)
        s2_tex = MathTex(r"S = 2.00", font_size=40, color="#44aaff"
                         ).next_to(center, DOWN, buff=0.8)
        self.play(Transform(init_needle, n2), Transform(s_display, s2_tex), run_time=1.5)
        self.play(Flash(needle_dot, color="#44aaff", flash_radius=0.3), run_time=0.5)
        self.wait(0.3)

        # Sweep to Tsirelson (S=2√2)
        n_ts = get_needle(2 * np.sqrt(2))
        s_ts_tex = MathTex(r"S = 2\sqrt{2} \approx 2.83", font_size=40, color="#aa44ff"
                           ).next_to(center, DOWN, buff=0.8)
        self.play(Transform(init_needle, n_ts), Transform(s_display, s_ts_tex), run_time=1.5)
        self.play(Flash(needle_dot, color="#aa44ff", flash_radius=0.4), run_time=0.5)

        # Tsirelson bound annotation
        self.play(Write(tsirelson_def), run_time=1)
        self.wait(0.3)

        # Try to push into forbidden zone → bounces back
        n4 = get_needle(3.5)
        s4_tex = MathTex(r"S = 3.50", font_size=40, color="#ff4444"
                         ).next_to(center, DOWN, buff=0.8)
        self.play(Transform(init_needle, n4), Transform(s_display, s4_tex),
                  run_time=0.8, rate_func=rush_into)

        # Bounce back!
        self.play(Transform(init_needle, n_ts.copy()), Transform(s_display, s_ts_tex.copy()),
                  run_time=0.6, rate_func=rush_from)
        self.play(Wiggle(init_needle, scale_value=1.05, rotation_angle=0.03), run_time=0.6)

        self.play(FadeIn(bounds_text, shift=LEFT*0.3), run_time=1)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene 2: PR-Box Crime   →  assets/s2_prbox_crime.webm
# Animated truth table: shows all xy combos,
# the XOR rule a⊕b = xy, and accumulates S = 4.
# Then a "VIOLATION" stamp appears.
# ─────────────────────────────────────────────────────────
class PRBoxCrime(Scene):
    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("PR-Box: The Perfect Crime", font_size=38, color=YELLOW,
                      weight=BOLD).to_edge(UP, buff=0.5)
        subtitle = MathTex(r"\text{Correlation rule: } a \oplus b = x \cdot y",
                           font_size=28, color=GREY_B).next_to(title, DOWN, buff=0.2)
        self.play(Write(title), FadeIn(subtitle), run_time=1)

        # ── Truth table ──
        header_data = ["x", "y", "x \\cdot y", "a \\oplus b", "\\text{Win?}"]
        rows_data = [
            ["0", "0", "0", "0", "\\checkmark"],
            ["0", "1", "0", "0", "\\checkmark"],
            ["1", "0", "0", "0", "\\checkmark"],
            ["1", "1", "1", "1", "\\checkmark"],
        ]

        col_colors = [TEAL, TEAL, ORANGE, ORANGE, GREEN]

        table_group = VGroup()
        col_widths = [1.2, 1.2, 1.5, 1.5, 1.3]
        row_height = 0.7
        x_start = -3.2
        y_start = 1.2

        # Header
        header_row = VGroup()
        x_pos = x_start
        for i, (hd, cw) in enumerate(zip(header_data, col_widths)):
            cell = MathTex(hd, font_size=26, color=col_colors[i])
            cell.move_to([x_pos + cw/2, y_start, 0])
            header_row.add(cell)
            x_pos += cw
        header_line = Line([x_start, y_start - 0.35, 0],
                           [x_pos, y_start - 0.35, 0],
                           color=GREY_D, stroke_width=1.5)

        # Data rows
        data_rows = VGroup()
        for r, row in enumerate(rows_data):
            row_group = VGroup()
            x_pos = x_start
            for i, (val, cw) in enumerate(zip(row, col_widths)):
                col = col_colors[i]
                if val == "\\checkmark":
                    cell = MathTex(val, font_size=28, color=GREEN)
                else:
                    cell = MathTex(val, font_size=28, color=col)
                cell.move_to([x_pos + cw/2, y_start - 0.7 - r * row_height, 0])
                row_group.add(cell)
                x_pos += cw
            data_rows.add(row_group)

        # ── S counter (right side) ──
        s_counter_title = Text("CHSH Score", font_size=22, color=WHITE,
                               weight=BOLD).shift(RIGHT*4 + UP*1.5)
        s_values = []
        for i in range(5):
            s_val = MathTex(f"S = {i}", font_size=36,
                            color=GREEN if i < 4 else YELLOW
                            ).shift(RIGHT*4 + UP*0.6)
            s_values.append(s_val)

        # ── Build animation ──
        self.play(FadeIn(header_row), Create(header_line), run_time=0.8)
        self.play(FadeIn(s_counter_title), FadeIn(s_values[0]), run_time=0.5)

        # Reveal each row, increment counter
        for r in range(4):
            self.play(FadeIn(data_rows[r], shift=RIGHT*0.3), run_time=0.6)
            new_s = s_values[r + 1]
            self.play(Transform(s_values[0], new_s), run_time=0.4)
            if r < 3:
                self.wait(0.2)

        self.wait(0.3)

        # ── S = 4 highlight ──
        s_final = MathTex(r"S = 4", font_size=48, color=YELLOW
                          ).shift(RIGHT*4 + UP*0.6)
        self.play(Transform(s_values[0], s_final), run_time=0.5)
        self.play(Circumscribe(s_final, color=YELLOW, buff=0.15), run_time=0.8)

        # ── Comparison bars (bottom) ──
        bar_group = VGroup()
        bar_data = [
            ("Classical", 2, "#44aaff"),
            ("Tsirelson", 2*np.sqrt(2), "#aa44ff"),
            ("PR-Box", 4, "#ff4444"),
        ]
        bar_width = 1.0
        max_w = 5.5
        base_x = -3.5
        base_y = -2.2

        for i, (name, val, col) in enumerate(bar_data):
            y = base_y - i * 0.7
            w = (val / 4) * max_w
            bar = Rectangle(width=w, height=0.4, color=col, fill_color=col,
                            fill_opacity=0.5, stroke_width=2)
            bar.move_to([base_x + w/2, y, 0])
            lbl = Text(name, font_size=16, color=col).next_to(bar, LEFT, buff=0.15)
            val_lbl = MathTex(f"S={val:.2f}" if val != 4 else "S=4", font_size=18,
                              color=WHITE).next_to(bar, RIGHT, buff=0.15)
            bar_group.add(VGroup(bar, lbl, val_lbl))

        self.play(LaggedStartMap(FadeIn, bar_group, lag_ratio=0.3), run_time=1.5)

        # Tsirelson line
        ts_x = base_x + (2*np.sqrt(2)/4)*max_w
        ts_line = DashedLine([ts_x, base_y + 0.4, 0], [ts_x, base_y - 1.8, 0],
                             color=YELLOW, stroke_width=2, dash_length=0.1)
        ts_lbl = Text("Tsirelson", font_size=14, color=YELLOW
                      ).next_to(ts_line, UP, buff=0.1)
        self.play(Create(ts_line), FadeIn(ts_lbl), run_time=0.8)

        # ── VIOLATION stamp ──
        stamp = Text("VIOLATION", font_size=60, color="#ff4444",
                     weight=BOLD, font="Courier New").rotate(15*DEGREES)
        stamp.move_to(ORIGIN + RIGHT*0.5)
        stamp_border = SurroundingRectangle(stamp, color="#ff4444",
                                            stroke_width=4, buff=0.2, corner_radius=0.1)
        stamp_group = VGroup(stamp_border, stamp)
        stamp_group.set_opacity(0)

        self.play(stamp_group.animate.set_opacity(0.85), run_time=0.5,
                  rate_func=rush_into)
        self.play(Wiggle(stamp_group, scale_value=1.05), run_time=0.6)

        # "But it respects no-signaling!"
        ns_text = Text("Yet it respects No-Signaling!", font_size=22,
                        color=GREY_B).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(ns_text, shift=UP*0.2), run_time=0.8)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene 3: IC Game   →  assets/s2_ic_game.webm
# Information Causality game animated:
# Alice bits → channel → Bob guess → I accumulates → then
# shows QM passes and PR-box fails.
# ─────────────────────────────────────────────────────────
class ICGame(Scene):
    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("Information Causality", font_size=38, color=WHITE,
                     weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.7)

        # ── Alice ──
        alice_box = RoundedRectangle(corner_radius=0.15, width=3.0, height=4.0,
                                     color=TEAL, fill_color="#0a2a2a",
                                     fill_opacity=0.9, stroke_width=2.5
                                     ).shift(LEFT*4.5 + DOWN*0.3)
        alice_lbl = Text("Alice", font_size=24, color=TEAL,
                         weight=BOLD).next_to(alice_box, UP, buff=0.15)

        # Alice's bits
        n_bits = 4
        bit_group = VGroup()
        for i in range(n_bits):
            bit_sq = Square(side_length=0.5, color=TEAL, fill_opacity=0.25, stroke_width=2)
            bit_tx = MathTex(f"a_{i}", font_size=20, color=WHITE)
            bit = VGroup(bit_sq, bit_tx).arrange(ORIGIN)
            bit_group.add(bit)
        bit_group.arrange(RIGHT, buff=0.15).move_to(alice_box.get_center() + UP*0.8)
        bits_label = MathTex(r"\vec{a} = (a_0, \ldots, a_{N-1})", font_size=22,
                             color=TEAL).move_to(alice_box.get_center() + DOWN*0.1)
        alice_note = Text("N random bits", font_size=16, color=GREY_B
                          ).move_to(alice_box.get_center() + DOWN*0.7)

        # ── Channel ──
        channel_arrow = Arrow(LEFT*2.5, RIGHT*0.0, color=ORANGE,
                              stroke_width=4, buff=0,
                              max_tip_length_to_length_ratio=0.1
                              ).shift(DOWN*0.3 + LEFT*0.2)
        ch_label = MathTex(r"\vec{x}", font_size=30, color=ORANGE
                           ).next_to(channel_arrow, UP, buff=0.15)
        ch_desc = Text("m classical bits", font_size=16, color=ORANGE
                       ).next_to(channel_arrow, DOWN, buff=0.15)

        # ── Bob ──
        bob_box = RoundedRectangle(corner_radius=0.15, width=3.0, height=4.0,
                                   color="#44aaff", fill_color="#0a1a2e",
                                   fill_opacity=0.9, stroke_width=2.5
                                   ).shift(RIGHT*4.0 + DOWN*0.3)
        bob_lbl = Text("Bob", font_size=24, color="#44aaff",
                       weight=BOLD).next_to(bob_box, UP, buff=0.15)

        b_input = MathTex(r"b \in \{0,\ldots,N{-}1\}", font_size=20,
                          color=WHITE).move_to(bob_box.get_center() + UP*0.8)
        b_desc = Text("random index", font_size=16, color=GREY_B
                      ).next_to(b_input, DOWN, buff=0.15)
        beta_out = MathTex(r"\beta = \text{guess of } a_b", font_size=20,
                           color=YELLOW).move_to(bob_box.get_center() + DOWN*0.5)

        # ── Shared resource ──
        resource_line = DashedLine(LEFT*4.5 + DOWN*2.8, RIGHT*4.0 + DOWN*2.8,
                                   color="#aa44ff", stroke_width=2, dash_length=0.15)
        resource_lbl = Text("Shared No-Signaling Resource", font_size=16,
                            color="#aa44ff").next_to(resource_line, DOWN, buff=0.1)

        # ── Performance quantity ──
        perf_box = RoundedRectangle(corner_radius=0.1, width=10, height=1.2,
                                    color="#aa44ff", fill_color="#1a0a2e",
                                    fill_opacity=0.8, stroke_width=2
                                    ).to_edge(DOWN, buff=0.3)
        perf_eq = MathTex(
            r"I = \sum_{i=0}^{N-1} I_{\text{Sh}}(a_i : \beta \mid b=i)",
            font_size=26, color=WHITE
        ).move_to(perf_box.get_center() + LEFT*1.5)
        perf_rule = MathTex(r"\leq m", font_size=30, color=GREEN
                            ).next_to(perf_eq, RIGHT, buff=0.3)

        # ============== ANIMATION ==============
        # Alice
        self.play(Create(alice_box), Write(alice_lbl), run_time=0.7)
        self.play(LaggedStartMap(FadeIn, bit_group, lag_ratio=0.1), run_time=0.8)
        self.play(Write(bits_label), FadeIn(alice_note), run_time=0.7)

        # Channel
        self.play(GrowArrow(channel_arrow), Write(ch_label), FadeIn(ch_desc), run_time=0.8)

        # Bob
        self.play(Create(bob_box), Write(bob_lbl), run_time=0.7)
        self.play(Write(b_input), FadeIn(b_desc), Write(beta_out), run_time=0.8)

        # Resource
        self.play(Create(resource_line), FadeIn(resource_lbl), run_time=0.8)
        self.wait(0.3)

        # Performance quantity
        self.play(Create(perf_box), Write(perf_eq), run_time=1)
        self.play(Write(perf_rule), run_time=0.6)
        self.play(Circumscribe(VGroup(perf_eq, perf_rule), color=GREEN, buff=0.1), run_time=0.8)

        self.wait(0.3)

        # ── Verdict panel (right edge) ──
        verdict_qm = VGroup(
            Text("Quantum:", font_size=18, color="#aa44ff", weight=BOLD),
            MathTex(r"I \leq m", font_size=22, color=GREEN),
            Text("  PASS", font_size=16, color=GREEN, weight=BOLD),
        ).arrange(RIGHT, buff=0.2).shift(RIGHT*4 + DOWN*1.5)

        verdict_pr = VGroup(
            Text("PR-Box:", font_size=18, color="#ff4444", weight=BOLD),
            MathTex(r"I > m", font_size=22, color="#ff4444"),
            Text("  FAIL", font_size=16, color="#ff4444", weight=BOLD),
        ).arrange(RIGHT, buff=0.2).next_to(verdict_qm, DOWN, buff=0.25)

        self.play(FadeIn(verdict_qm, shift=LEFT*0.3), run_time=0.8)
        self.play(FadeIn(verdict_pr, shift=LEFT*0.3), run_time=0.8)
        self.play(Indicate(verdict_pr, color="#ff4444", scale_factor=1.05), run_time=0.8)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene 4: DPI Chain   →  assets/s2_dpi_chain.webm
# Animated logical chain:
# DPI → Information Causality → Tsirelson's Bound
# with PR-box being excluded at each step.
# ─────────────────────────────────────────────────────────
class DPIChain(Scene):
    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("The Logical Chain", font_size=38, color=WHITE,
                     weight=BOLD).to_edge(UP, buff=0.4)
        subtitle = Text("How DPI implies Tsirelson's Bound", font_size=22,
                        color=GREY_B).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(subtitle), run_time=0.8)

        # ── Three boxes in a chain ──
        box_style = dict(corner_radius=0.15, width=4.0, height=2.0,
                         fill_opacity=0.9, stroke_width=2.5)

        # Box 1: DPI
        dpi_box = RoundedRectangle(color="#ff9800", fill_color="#2e1a0a",
                                   **box_style).shift(LEFT*4.5 + UP*0.3)
        dpi_title = Text("DPI", font_size=28, color="#ff9800",
                         weight=BOLD).move_to(dpi_box.get_center() + UP*0.4)
        dpi_eq = MathTex(r"H(A|B) \leq H(A|T(B))", font_size=20,
                         color=GREY_B).move_to(dpi_box.get_center() + DOWN*0.2)
        dpi_desc = Text("+ COND + SHAN", font_size=14, color=GREY_D
                        ).move_to(dpi_box.get_center() + DOWN*0.55)

        # Box 2: IC
        ic_box = RoundedRectangle(color="#aa44ff", fill_color="#1a0a2e",
                                  **box_style).shift(UP*0.3)
        ic_title = Text("Information\nCausality", font_size=24, color="#aa44ff",
                        weight=BOLD).move_to(ic_box.get_center() + UP*0.3)
        ic_eq = MathTex(r"I \leq m", font_size=22, color=GREY_B
                        ).move_to(ic_box.get_center() + DOWN*0.35)

        # Box 3: Tsirelson
        ts_box = RoundedRectangle(color="#44aaff", fill_color="#0a1a2e",
                                  **box_style).shift(RIGHT*4.5 + UP*0.3)
        ts_title = Text("Tsirelson's\nBound", font_size=24, color="#44aaff",
                        weight=BOLD).move_to(ts_box.get_center() + UP*0.3)
        ts_eq = MathTex(r"S \leq 2\sqrt{2}", font_size=22, color=GREY_B
                        ).move_to(ts_box.get_center() + DOWN*0.35)

        # ── Arrows ──
        arrow1 = Arrow(dpi_box.get_right(), ic_box.get_left(),
                       color=YELLOW, stroke_width=4, buff=0.1,
                       max_tip_length_to_length_ratio=0.15)
        arrow1_lbl = MathTex(r"\Rightarrow", font_size=36, color=YELLOW
                             ).next_to(arrow1, UP, buff=0.05)

        arrow2 = Arrow(ic_box.get_right(), ts_box.get_left(),
                       color=YELLOW, stroke_width=4, buff=0.1,
                       max_tip_length_to_length_ratio=0.15)
        arrow2_lbl = MathTex(r"\Rightarrow", font_size=36, color=YELLOW
                             ).next_to(arrow2, UP, buff=0.05)
        cite_lbl = Text("[Pawłowski et al.]", font_size=12, color=GREY_D
                        ).next_to(arrow2, DOWN, buff=0.05)

        # ── PR-Box exclusion (below) ──
        pr_label = MathTex(r"\text{PR-Box } (S=4)", font_size=26, color="#ff4444"
                           ).shift(DOWN*2.2)
        cross1 = Line(pr_label.get_left() + LEFT*0.2 + DOWN*0.15,
                      pr_label.get_right() + RIGHT*0.2 + UP*0.15,
                      color="#ff4444", stroke_width=4)
        cross2 = Line(pr_label.get_left() + LEFT*0.2 + UP*0.15,
                      pr_label.get_right() + RIGHT*0.2 + DOWN*0.15,
                      color="#ff4444", stroke_width=4)

        # Arrows from PR to each box (blocked)
        pr_to_dpi = Arrow(pr_label.get_top() + LEFT*2, dpi_box.get_bottom(),
                          color="#ff4444", stroke_width=2, buff=0.1,
                          max_tip_length_to_length_ratio=0.15, stroke_opacity=0.5)
        pr_to_ic = Arrow(pr_label.get_top(), ic_box.get_bottom(),
                         color="#ff4444", stroke_width=2, buff=0.1,
                         max_tip_length_to_length_ratio=0.15, stroke_opacity=0.5)
        pr_to_ts = Arrow(pr_label.get_top() + RIGHT*2, ts_box.get_bottom(),
                         color="#ff4444", stroke_width=2, buff=0.1,
                         max_tip_length_to_length_ratio=0.15, stroke_opacity=0.5)

        # X marks on arrows
        x_marks = VGroup()
        for arrow in [pr_to_dpi, pr_to_ic, pr_to_ts]:
            mid = arrow.get_center()
            xm = MathTex(r"\times", font_size=30, color="#ff4444").move_to(mid)
            x_marks.add(xm)

        # ── Key insight (bottom) ──
        insight_box = RoundedRectangle(corner_radius=0.1, width=11, height=0.8,
                                       color=YELLOW, fill_color="#2e2a0a",
                                       fill_opacity=0.6, stroke_width=2
                                       ).to_edge(DOWN, buff=0.2)
        insight_text = Text(
            "The real constraint is information-theoretic, not just relativistic!",
            font_size=18, color=YELLOW, weight=BOLD
        ).move_to(insight_box.get_center())

        # ============== ANIMATION ==============
        # Box 1: DPI
        self.play(Create(dpi_box), Write(dpi_title), run_time=0.8)
        self.play(Write(dpi_eq), FadeIn(dpi_desc), run_time=0.7)
        self.wait(0.3)

        # Arrow 1
        self.play(GrowArrow(arrow1), FadeIn(arrow1_lbl), run_time=0.8)

        # Box 2: IC
        self.play(Create(ic_box), Write(ic_title), run_time=0.8)
        self.play(Write(ic_eq), run_time=0.5)
        self.wait(0.3)

        # Arrow 2
        self.play(GrowArrow(arrow2), FadeIn(arrow2_lbl), FadeIn(cite_lbl), run_time=0.8)

        # Box 3: Tsirelson
        self.play(Create(ts_box), Write(ts_title), run_time=0.8)
        self.play(Write(ts_eq), run_time=0.5)

        # Highlight the whole chain
        self.play(
            Indicate(dpi_box, color="#ff9800", scale_factor=1.03),
            Indicate(ic_box, color="#aa44ff", scale_factor=1.03),
            Indicate(ts_box, color="#44aaff", scale_factor=1.03),
            run_time=1
        )
        self.wait(0.3)

        # PR-Box exclusion
        self.play(Write(pr_label), run_time=0.6)
        self.play(
            Create(pr_to_dpi), Create(pr_to_ic), Create(pr_to_ts),
            run_time=0.8
        )
        self.play(
            FadeIn(x_marks),
            Create(cross1), Create(cross2),
            run_time=0.8
        )
        self.wait(0.3)

        # Key insight
        self.play(Create(insight_box), Write(insight_text), run_time=1)
        self.play(Indicate(insight_box, color=YELLOW, scale_factor=1.02), run_time=0.8)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene 5: Entropy definition visual → assets/s2_entropy.webm
# Shows H(P) = min over fine-grained measurements of H_Sh
# with a visual of measurement outcomes and Shannon entropy
# ─────────────────────────────────────────────────────────
class EntropyDef(Scene):
    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("Generalized Entropy", font_size=36, color=WHITE,
                     weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.7)

        # ── Central idea ──
        idea = Text("Minimal uncertainty over all maximal measurements",
                    font_size=20, color=GREY_B).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(idea), run_time=0.5)

        # ── State blob ──
        state_circ = Circle(radius=1.0, color="#aa44ff", fill_color="#aa44ff",
                            fill_opacity=0.15, stroke_width=2.5).shift(LEFT*3.5)
        state_lbl = MathTex(r"\vec{P}", font_size=36, color="#aa44ff"
                            ).move_to(state_circ.get_center())
        state_desc = Text("State", font_size=16, color=GREY_B
                          ).next_to(state_circ, DOWN, buff=0.15)

        # ── Multiple measurement arrows ──
        measurements = VGroup()
        angles = [-30, 0, 30]
        meas_labels = [r"e_1", r"e_2", r"e_3"]
        bar_charts = []

        for i, (ang, ml) in enumerate(zip(angles, meas_labels)):
            direction = np.array([np.cos(ang*DEGREES), np.sin(ang*DEGREES), 0])
            start = state_circ.get_center() + 1.1 * direction
            end = start + 2.0 * direction
            arr = Arrow(start, end, color=GREY_B, stroke_width=2, buff=0,
                        max_tip_length_to_length_ratio=0.12)
            lbl = MathTex(ml, font_size=18, color=GREY_B
                          ).next_to(arr, UP if ang >= 0 else DOWN, buff=0.05)
            measurements.add(VGroup(arr, lbl))

            # Mini bar chart at the end
            bars = VGroup()
            heights_options = [
                [0.6, 0.3, 0.1],   # low entropy
                [0.35, 0.35, 0.3],  # high entropy (most uniform)
                [0.5, 0.4, 0.1],    # medium entropy
            ]
            h_values = heights_options[i]
            for j, h in enumerate(h_values):
                bar = Rectangle(width=0.2, height=h*1.5, color="#00ccff",
                                fill_color="#00ccff", fill_opacity=0.5, stroke_width=1)
                bars.add(bar)
            bars.arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
            bars.next_to(end + 0.3*direction, direction, buff=0.1)
            bar_charts.append(bars)

        # ── Shannon entropy values ──
        h_vals_tex = VGroup()
        h_val_nums = [1.36, 1.58, 1.45]
        for i, (bc, hv) in enumerate(zip(bar_charts, h_val_nums)):
            tex = MathTex(f"H_{{\\text{{Sh}}}} = {hv:.2f}", font_size=16,
                          color="#00ccff").next_to(bc, DOWN, buff=0.1)
            h_vals_tex.add(tex)

        # ── Result: minimum ──
        result_box = RoundedRectangle(corner_radius=0.1, width=6, height=1.8,
                                      color="#aa44ff", fill_color="#1a0a2e",
                                      fill_opacity=0.9, stroke_width=2
                                      ).shift(DOWN*2.2)
        result_eq = MathTex(
            r"H(\vec{P}) = \min_{e \in \mathcal{M}^*} H_{\text{Sh}}(e(\vec{P}))",
            font_size=26, color=WHITE
        ).move_to(result_box.get_center() + UP*0.2)
        result_note = Text("Minimized over all fine-grained measurements",
                           font_size=14, color=GREY_B
                           ).move_to(result_box.get_center() + DOWN*0.35)

        # ── Properties (right side) ──
        props = VGroup(
            MathTex(r"\bullet\; \text{Classical} \to H_{\text{Sh}}", font_size=20, color="#55ff99"),
            MathTex(r"\bullet\; \text{Quantum} \to H_{\text{vN}}", font_size=20, color="#55ff99"),
            MathTex(r"\bullet\; 0 \leq H(\vec{P}) \leq \log d", font_size=20, color=GREY_B),
            MathTex(r"\bullet\; \text{Concavity holds}", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5).shift(UP*0.3)

        # ============== ANIMATION ==============
        self.play(Create(state_circ), Write(state_lbl), FadeIn(state_desc), run_time=0.8)

        # Measurement arrows + bar charts
        for i in range(3):
            self.play(GrowArrow(measurements[i][0]), Write(measurements[i][1]),
                      run_time=0.5)
            self.play(LaggedStartMap(FadeIn, bar_charts[i],
                                     lag_ratio=0.15), run_time=0.5)
            self.play(Write(h_vals_tex[i]), run_time=0.3)

        self.wait(0.3)

        # Highlight the minimum
        min_highlight = SurroundingRectangle(h_vals_tex[0], color=YELLOW,
                                             buff=0.08, stroke_width=2)
        min_label = Text("MIN", font_size=14, color=YELLOW, weight=BOLD
                         ).next_to(min_highlight, DOWN, buff=0.05)
        self.play(Create(min_highlight), FadeIn(min_label), run_time=0.6)

        # Result
        self.play(Create(result_box), Write(result_eq), FadeIn(result_note), run_time=1.2)

        # Properties
        self.play(LaggedStartMap(FadeIn, props, lag_ratio=0.2), run_time=1)

        self.wait(2)
