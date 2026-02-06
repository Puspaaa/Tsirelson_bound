"""
Manim animations for individual lemma visual aids.
Each scene illustrates the core idea behind one lemma.

Run:
  manim -qh --format=webm -o <name>.webm manim_lemmas.py <Scene>
"""

from manim import *
import numpy as np


# ─────────────────────────────────────────────────────────
# Scene 1: Lemma3Visual → s4_lemma3_subadditivity.webm
# Visual: joint system splits into parts; total entropy
# of parts >= joint entropy (like cutting a rope)
# ─────────────────────────────────────────────────────────
class Lemma3Visual(Scene):
    def construct(self):
        self.camera.background_color = "#0f1729"

        title = Text("Lemma 3 — Subadditivity", font_size=36, color=WHITE,
                     weight=BOLD).to_edge(UP, buff=0.4)
        subtitle = Text("Individual uncertainties sum to more than joint uncertainty",
                        font_size=18, color="#6b7d8f").next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(subtitle), run_time=0.8)

        # Statement
        statement = MathTex(
            r"\sum_{i=1}^{n} H(A_i|\gamma) \;\geq\; H(A_1 A_2 \ldots A_n | \gamma)",
            font_size=30, color="#5b9bf5"
        ).shift(UP * 1.5)
        box = SurroundingRectangle(statement, color="#5b9bf5", buff=0.2,
                                   corner_radius=0.1, stroke_width=1.5)
        self.play(Write(statement), Create(box), run_time=1)
        self.wait(0.3)

        # Visual: A big box representing joint system A1...An|γ
        joint_box = RoundedRectangle(
            corner_radius=0.15, width=8, height=2.2,
            color="#a78bfa", fill_color="#1e2a3a", fill_opacity=0.8,
            stroke_width=2.5
        ).shift(DOWN * 0.3)
        joint_label = MathTex(r"H(A_1 A_2 \ldots A_n | \gamma)",
                              font_size=22, color="#a78bfa").move_to(joint_box)

        # Sub-boxes inside representing individual A_i
        colors = ["#5b9bf5", "#5ae4a7", "#fb923c", "#f87171"]
        sub_boxes = VGroup()
        sub_labels = VGroup()
        for i in range(4):
            sb = RoundedRectangle(
                corner_radius=0.1, width=1.7, height=1.6,
                color=colors[i], fill_color="#182030", fill_opacity=0.9,
                stroke_width=2
            )
            sl = MathTex(f"A_{i+1}", font_size=20, color=colors[i]).move_to(sb)
            sub_boxes.add(sb)
            sub_labels.add(sl)
        sub_group = VGroup(*[VGroup(b, l) for b, l in zip(sub_boxes, sub_labels)])
        sub_group.arrange(RIGHT, buff=0.3).move_to(joint_box)

        # Show joint box first
        self.play(Create(joint_box), Write(joint_label), run_time=0.8)
        self.wait(0.5)

        # Transform: split into individual boxes
        self.play(FadeOut(joint_label), run_time=0.3)
        self.play(
            ReplacementTransform(joint_box, sub_boxes),
            LaggedStartMap(FadeIn, sub_labels, lag_ratio=0.2),
            run_time=1.2
        )
        self.wait(0.3)

        # Show individual entropies stacking up (bar chart)
        bars = VGroup()
        bar_labels = VGroup()
        bar_x_start = -3.5
        total_h = 0
        heights = [1.0, 0.8, 1.1, 0.7]
        for i in range(4):
            h = heights[i]
            total_h += h
            bar = Rectangle(
                width=0.8, height=h, color=colors[i],
                fill_color=colors[i], fill_opacity=0.6, stroke_width=1.5
            ).move_to(DOWN * 2.8 + RIGHT * (bar_x_start + i * 1.2) + UP * h / 2)
            bl = MathTex(f"H(A_{i+1}|\\gamma)", font_size=12, color=colors[i]
                         ).next_to(bar, DOWN, buff=0.1)
            bars.add(bar)
            bar_labels.add(bl)

        # Joint entropy bar (shorter)
        joint_h = total_h * 0.65
        joint_bar = Rectangle(
            width=1.2, height=joint_h, color="#a78bfa",
            fill_color="#a78bfa", fill_opacity=0.6, stroke_width=1.5
        ).move_to(DOWN * 2.8 + RIGHT * 2.5 + UP * joint_h / 2)
        joint_bl = MathTex(r"H(\text{joint}|\gamma)", font_size=12, color="#a78bfa"
                           ).next_to(joint_bar, DOWN, buff=0.1)

        # Inequality
        geq = MathTex(r"\geq", font_size=36, color="#fbbf24"
                      ).move_to(DOWN * 2.5 + RIGHT * 1.2)

        bar_anims = [GrowFromEdge(b, DOWN) for b in bars]
        self.play(
            LaggedStart(*bar_anims, lag_ratio=0.15),
            LaggedStartMap(FadeIn, bar_labels, lag_ratio=0.15),
            run_time=1
        )
        self.play(
            GrowFromEdge(joint_bar, DOWN), FadeIn(joint_bl),
            Write(geq),
            run_time=0.8
        )

        # Insight text
        insight = Text(
            "Correlations between parts are lost when measuring individually",
            font_size=16, color="#fbbf24"
        ).shift(DOWN * 3.5)
        self.play(FadeIn(insight), run_time=0.6)

        self.wait(2.5)


# ─────────────────────────────────────────────────────────
# Scene 2: Lemma4Visual → s4_lemma4_product.webm
# Visual: Two independent systems — entropies factorize
# ─────────────────────────────────────────────────────────
class Lemma4Visual(Scene):
    def construct(self):
        self.camera.background_color = "#0f1729"

        title = Text("Lemma 4 — Product State Independence", font_size=36,
                     color=WHITE, weight=BOLD).to_edge(UP, buff=0.4)
        subtitle = Text("For product states, conditioning on B tells nothing about A",
                        font_size=18, color="#6b7d8f").next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(subtitle), run_time=0.8)

        # Statement
        statement = MathTex(
            r"H(A|B) = H(A) \quad \text{for } \vec{P}_A \otimes \vec{P}_B",
            font_size=30, color="#5ae4a7"
        ).shift(UP * 1.5)
        box = SurroundingRectangle(statement, color="#5ae4a7", buff=0.2,
                                   corner_radius=0.1, stroke_width=1.5)
        self.play(Write(statement), Create(box), run_time=1)
        self.wait(0.3)

        # Visual: Two blobs (system A and system B) — independent
        blob_a = Circle(radius=1.2, color="#5b9bf5", fill_color="#182030",
                        fill_opacity=0.8, stroke_width=2.5).shift(LEFT * 2.5 + DOWN * 0.5)
        label_a = MathTex(r"\vec{P}_A", font_size=28, color="#5b9bf5").move_to(blob_a)
        letter_a = Text("A", font_size=40, color="#5b9bf5", weight=BOLD
                        ).next_to(blob_a, UP, buff=0.15)

        blob_b = Circle(radius=1.2, color="#fb923c", fill_color="#182030",
                        fill_opacity=0.8, stroke_width=2.5).shift(RIGHT * 2.5 + DOWN * 0.5)
        label_b = MathTex(r"\vec{P}_B", font_size=28, color="#fb923c").move_to(blob_b)
        letter_b = Text("B", font_size=40, color="#fb923c", weight=BOLD
                        ).next_to(blob_b, UP, buff=0.15)

        # Tensor product symbol between
        tensor = MathTex(r"\otimes", font_size=50, color="#6b7d8f").move_to(DOWN * 0.5)

        self.play(
            Create(blob_a), Write(label_a), Write(letter_a),
            Create(blob_b), Write(label_b), Write(letter_b),
            Write(tensor),
            run_time=1
        )
        self.wait(0.3)

        # Show "no connection" — dashed line with X
        no_conn = DashedLine(
            blob_a.get_right(), blob_b.get_left(),
            color="#f87171", stroke_width=2, dash_length=0.15
        )
        cross = VGroup(
            Line(UP * 0.2 + LEFT * 0.2, DOWN * 0.2 + RIGHT * 0.2, color="#f87171", stroke_width=3),
            Line(UP * 0.2 + RIGHT * 0.2, DOWN * 0.2 + LEFT * 0.2, color="#f87171", stroke_width=3),
        ).move_to(ORIGIN + DOWN * 0.5)

        self.play(Create(no_conn), Create(cross), FadeOut(tensor), run_time=0.7)

        no_corr = Text("No correlations", font_size=16, color="#f87171"
                       ).next_to(cross, DOWN, buff=0.15)
        self.play(FadeIn(no_corr), run_time=0.4)
        self.wait(0.3)

        # Arrow annotation: measuring B doesn't reduce H(A)
        arrow_down = Line(
            blob_b.get_bottom() + DOWN * 0.1,
            blob_b.get_bottom() + DOWN * 0.8,
            color="#fb923c", stroke_width=2
        )
        measure_label = Text("Measure B", font_size=16, color="#fb923c"
                             ).next_to(arrow_down, DOWN, buff=0.1)

        unchanged = VGroup(
            MathTex(r"H(A|B)", font_size=22, color="#5ae4a7"),
            MathTex(r"=", font_size=22, color=WHITE),
            MathTex(r"H(A)", font_size=22, color="#5ae4a7"),
        ).arrange(RIGHT, buff=0.15).shift(DOWN * 2.8)
        unchanged_note = Text("Uncertainty about A unchanged!", font_size=16,
                              color="#fbbf24").next_to(unchanged, DOWN, buff=0.2)

        self.play(Create(arrow_down), Write(measure_label), run_time=0.6)
        self.play(Write(unchanged), run_time=0.7)
        self.play(FadeIn(unchanged_note), run_time=0.5)

        # Proof sketch at bottom
        proof_note = VGroup(
            Text("Proof uses:", font_size=14, color="#6b7d8f"),
            Text("COND to write H(A|B) = H(AB) - H(B)", font_size=13, color="#a78bfa"),
            Text("SHAN to evaluate classical marginals", font_size=13, color="#fbbf24"),
            Text("DPI to bound processing of product states", font_size=13, color="#f87171"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).shift(DOWN * 3.7)

        self.play(FadeIn(proof_note), run_time=0.6)
        self.wait(2.5)


# ─────────────────────────────────────────────────────────
# Scene 3: Lemma5Visual → s4_lemma5_positivity.webm
# Visual: Conditional entropy is non-negative for classical
# ─────────────────────────────────────────────────────────
class Lemma5Visual(Scene):
    def construct(self):
        self.camera.background_color = "#0f1729"

        title = Text("Lemma 5 — Positivity of Conditional Entropy", font_size=36,
                     color=WHITE, weight=BOLD).to_edge(UP, buff=0.4)
        subtitle = Text("Classical variable X always has non-negative conditional entropy",
                        font_size=18, color="#6b7d8f").next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(subtitle), run_time=0.8)

        # Statement
        statement = MathTex(
            r"H(X|Y) \geq 0 \quad \text{for classical } X",
            font_size=30, color="#fb923c"
        ).shift(UP * 1.5)
        box = SurroundingRectangle(statement, color="#fb923c", buff=0.2,
                                   corner_radius=0.1, stroke_width=1.5)
        self.play(Write(statement), Create(box), run_time=1)
        self.wait(0.3)

        # Visual: Two scenarios side by side
        # Left: Classical world (X can be cloned)
        left_title = Text("Classical X — Clonable", font_size=20,
                          color="#5ae4a7", weight=BOLD).shift(LEFT * 3.5 + UP * 0.3)

        # Show X as a document icon that gets cloned
        doc_x = RoundedRectangle(
            corner_radius=0.1, width=1.0, height=1.4,
            color="#5ae4a7", fill_color="#182030", fill_opacity=0.9,
            stroke_width=2
        ).shift(LEFT * 4.5 + DOWN * 0.8)
        doc_x_label = Text("X", font_size=22, color="#5ae4a7").move_to(doc_x)

        # Clone arrow
        clone_arrow = Line(
            doc_x.get_right() + RIGHT * 0.1,
            doc_x.get_right() + RIGHT * 1.2,
            color="#5ae4a7", stroke_width=2
        )
        clone_label = Text("clone", font_size=13, color="#5ae4a7"
                           ).next_to(clone_arrow, UP, buff=0.05)

        doc_x2 = doc_x.copy().shift(RIGHT * 1.6)
        doc_x2_label = Text("X'", font_size=22, color="#5ae4a7").move_to(doc_x2)

        self.play(Write(left_title), Create(doc_x), Write(doc_x_label), run_time=0.7)
        self.play(Create(clone_arrow), Write(clone_label), run_time=0.4)
        self.play(Create(doc_x2), Write(doc_x2_label), run_time=0.5)
        self.wait(0.2)

        # Right: Quantum world (no-cloning, can have H < 0)
        right_title = Text("Quantum — No Cloning!", font_size=20,
                           color="#f87171", weight=BOLD).shift(RIGHT * 3.5 + UP * 0.3)

        qubit = Circle(
            radius=0.5, color="#a78bfa", fill_color="#182030",
            fill_opacity=0.9, stroke_width=2
        ).shift(RIGHT * 2.5 + DOWN * 0.8)
        qubit_label = MathTex(r"|\psi\rangle", font_size=22, color="#a78bfa"
                              ).move_to(qubit)

        no_clone_arrow = Line(
            qubit.get_right() + RIGHT * 0.1,
            qubit.get_right() + RIGHT * 1.2,
            color="#f87171", stroke_width=2
        )
        cross_clone = VGroup(
            Line(UP * 0.15 + LEFT * 0.15, DOWN * 0.15 + RIGHT * 0.15,
                 color="#f87171", stroke_width=3),
            Line(UP * 0.15 + RIGHT * 0.15, DOWN * 0.15 + LEFT * 0.15,
                 color="#f87171", stroke_width=3),
        ).move_to(no_clone_arrow.get_center())

        can_neg = MathTex(r"H(X|Y) < 0 \text{ possible!}", font_size=18, color="#f87171"
                          ).shift(RIGHT * 3.5 + DOWN * 1.8)

        self.play(Write(right_title), Create(qubit), Write(qubit_label), run_time=0.7)
        self.play(Create(no_clone_arrow), Create(cross_clone), run_time=0.5)
        self.play(Write(can_neg), run_time=0.6)
        self.wait(0.3)

        # Divider
        divider = DashedLine(
            UP * 0.5, DOWN * 2.0, color="#2a3a4e", stroke_width=1.5, dash_length=0.1
        ).move_to(ORIGIN + DOWN * 0.5)
        self.play(Create(divider), run_time=0.3)

        # Key argument at bottom
        key_box = RoundedRectangle(
            corner_radius=0.1, width=10, height=1.8,
            color="#fbbf24", fill_color="#1e2a3a", fill_opacity=0.9,
            stroke_width=1.5
        ).shift(DOWN * 3.0)

        key_lines = VGroup(
            Text("Key argument:", font_size=18, color="#fbbf24", weight=BOLD),
            VGroup(
                Text("1. Clone classical X → X, X'", font_size=15, color="#b0bec5"),
                Text("2. Apply DPI: H(X|Y) ≥ H(X|YX') since YX' has more info", font_size=15, color="#b0bec5"),
                Text("3. But H(X|YX') ≥ 0 since X' = X determines X perfectly", font_size=15, color="#b0bec5"),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, buff=0.12).move_to(key_box)

        self.play(Create(key_box), Write(key_lines), run_time=1)
        self.wait(2.5)


# ─────────────────────────────────────────────────────────
# Scene 4: Lemma6Visual → s4_lemma6_ic_bound.webm
# Visual: The IC game with entropy flow
# ─────────────────────────────────────────────────────────
class Lemma6Visual(Scene):
    def construct(self):
        self.camera.background_color = "#0f1729"

        title = Text("Lemma 6 — The IC Bound", font_size=36,
                     color=WHITE, weight=BOLD).to_edge(UP, buff=0.4)
        subtitle = Text("Combining all lemmas to bound Bob's total information",
                        font_size=18, color="#6b7d8f").next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(subtitle), run_time=0.8)

        # Statement
        statement = MathTex(
            r"H(\vec{a}\,|\,B\vec{x}) \;\geq\; n - m",
            font_size=32, color="#a78bfa"
        ).shift(UP * 1.5)
        box = SurroundingRectangle(statement, color="#a78bfa", buff=0.2,
                                   corner_radius=0.1, stroke_width=1.5)
        self.play(Write(statement), Create(box), run_time=1)
        self.wait(0.3)

        # IC Game visual
        # Alice box
        alice_box = RoundedRectangle(
            corner_radius=0.12, width=2.5, height=2.0,
            color="#2dd4bf", fill_color="#182030", fill_opacity=0.9,
            stroke_width=2
        ).shift(LEFT * 4.5 + DOWN * 0.8)
        alice_title = Text("Alice", font_size=20, color="#2dd4bf", weight=BOLD
                           ).next_to(alice_box, UP, buff=0.1)

        # Alice's bits
        bits = VGroup()
        bit_vals = ["a₀", "a₁", "…", "aₙ₋₁"]
        for i, bv in enumerate(bit_vals):
            bt = Text(bv, font_size=16, color="#5b9bf5")
            bits.add(bt)
        bits.arrange(DOWN, buff=0.15).move_to(alice_box)
        n_label = MathTex(r"n \text{ bits}", font_size=16, color="#6b7d8f"
                          ).next_to(alice_box, DOWN, buff=0.1)

        # Channel
        channel = RoundedRectangle(
            corner_radius=0.1, width=2.0, height=1.0,
            color="#fb923c", fill_color="#1e2a3a", fill_opacity=0.9,
            stroke_width=2
        ).shift(DOWN * 0.8)
        channel_label = VGroup(
            Text("Channel", font_size=16, color="#fb923c", weight=BOLD),
            MathTex(r"m \text{ bits}", font_size=16, color="#6b7d8f"),
        ).arrange(DOWN, buff=0.05).move_to(channel)

        # Bob box
        bob_box = RoundedRectangle(
            corner_radius=0.12, width=2.5, height=2.0,
            color="#5b9bf5", fill_color="#182030", fill_opacity=0.9,
            stroke_width=2
        ).shift(RIGHT * 4.5 + DOWN * 0.8)
        bob_title = Text("Bob", font_size=20, color="#5b9bf5", weight=BOLD
                         ).next_to(bob_box, UP, buff=0.1)
        bob_content = VGroup(
            Text("Picks index b", font_size=14, color="#b0bec5"),
            Text("Guesses β(b)", font_size=14, color="#b0bec5"),
            MathTex(r"\beta \approx a_b \text{ ?}", font_size=18, color="#fbbf24"),
        ).arrange(DOWN, buff=0.12).move_to(bob_box)

        # Shared resource (entanglement below)
        shared = DashedLine(
            alice_box.get_bottom() + DOWN * 0.5,
            bob_box.get_bottom() + DOWN * 0.5,
            color="#a78bfa", stroke_width=1.5, dash_length=0.15
        ).shift(DOWN * 0.3)
        shared_label = Text("Shared non-local resource (e.g. entanglement)",
                            font_size=13, color="#a78bfa"
                            ).next_to(shared, DOWN, buff=0.08)

        # Arrows
        arrow1 = Line(
            alice_box.get_right(), channel.get_left(),
            color="#fb923c", stroke_width=2, buff=0.15
        )
        arrow2 = Line(
            channel.get_right(), bob_box.get_left(),
            color="#fb923c", stroke_width=2, buff=0.15
        )

        self.play(
            Create(alice_box), Write(alice_title), FadeIn(bits), FadeIn(n_label),
            run_time=0.8
        )
        self.play(
            Create(channel), FadeIn(channel_label),
            Create(arrow1), Create(arrow2),
            run_time=0.7
        )
        self.play(
            Create(bob_box), Write(bob_title), FadeIn(bob_content),
            run_time=0.8
        )
        self.play(Create(shared), FadeIn(shared_label), run_time=0.6)
        self.wait(0.3)

        # Derivation chain at bottom
        deriv_box = RoundedRectangle(
            corner_radius=0.1, width=11, height=1.6,
            color="#5b9bf5", fill_color="#0f1729", fill_opacity=0.95,
            stroke_width=1.5
        ).shift(DOWN * 3.2)

        deriv = VGroup(
            MathTex(r"\underbrace{H(\vec{a}|B\vec{x})}_{\text{Lemma 4,5}} \;\geq\; n - m",
                    font_size=20, color="#b0bec5"),
            MathTex(r"\xrightarrow{\text{Lemma 3}}",
                    font_size=18, color="#fbbf24"),
            MathTex(r"\sum_i H(a_i|\beta(i)) \geq n - m",
                    font_size=20, color="#b0bec5"),
            MathTex(r"\xrightarrow{\text{SHAN}}",
                    font_size=18, color="#fbbf24"),
            MathTex(r"I = \sum_i I(a_i:\beta(i)) \leq m",
                    font_size=20, color="#5ae4a7"),
        ).arrange(RIGHT, buff=0.2).move_to(deriv_box)

        self.play(Create(deriv_box), run_time=0.4)
        self.play(LaggedStartMap(FadeIn, deriv, lag_ratio=0.15), run_time=1.5)

        # Final highlight
        final = SurroundingRectangle(deriv[-1], color="#5ae4a7", buff=0.1,
                                      corner_radius=0.08, stroke_width=2)
        self.play(Create(final), run_time=0.5)

        self.wait(2.5)
