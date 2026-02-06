"""
Manim animations for Speaker 3: "The Proof & The Implications"
Covers: Proof sketch, Lemma chain, Box-world breakdown, Conclusion.

Run:
  manim -qh --format=webm -o <name>.webm manim_speaker3.py <Scene>
"""

from manim import *
import numpy as np


# ─────────────────────────────────────────────────────────
# Scene 1: ProofSketch  →  s3_proof_sketch.webm
# Shows the proof architecture: Lemmas feed into Theorem.
# ─────────────────────────────────────────────────────────
class ProofSketch(Scene):
    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("Proof Architecture", font_size=38, color=WHITE,
                     weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.7)

        # ── Axiom boxes at top ──
        axiom_style = dict(corner_radius=0.12, width=2.8, height=1.0,
                           fill_opacity=0.8, stroke_width=2.5)
        ax_cond = RoundedRectangle(color="#aa44ff", fill_color="#1a0a2e", **axiom_style)
        ax_shan = RoundedRectangle(color="#ffdd44", fill_color="#2e2a0a", **axiom_style)
        ax_dpi = RoundedRectangle(color="#ff5555", fill_color="#2e0a0a", **axiom_style)

        axioms = VGroup(ax_cond, ax_shan, ax_dpi).arrange(RIGHT, buff=0.8).shift(UP*3)
        ax_cond_t = VGroup(
            Text("COND", font_size=20, color="#aa44ff", weight=BOLD),
            MathTex(r"H(A|B)=H(AB){-}H(B)", font_size=16, color=GREY_B),
        ).arrange(DOWN, buff=0.1).move_to(ax_cond)
        ax_shan_t = VGroup(
            Text("SHAN", font_size=20, color="#ffdd44", weight=BOLD),
            MathTex(r"H_{\text{class}}=H_{\text{Sh}}", font_size=16, color=GREY_B),
        ).arrange(DOWN, buff=0.1).move_to(ax_shan)
        ax_dpi_t = VGroup(
            Text("DPI", font_size=20, color="#ff5555", weight=BOLD),
            MathTex(r"H(A|B)\leq H(A|T(B))", font_size=16, color=GREY_B),
        ).arrange(DOWN, buff=0.1).move_to(ax_dpi)

        # ── Lemma boxes (middle row) ──
        lem_style = dict(corner_radius=0.12, width=3.0, height=1.3,
                         fill_opacity=0.7, stroke_width=2)

        lemmas_data = [
            ("Lemma 3", r"\sum_i H(A_i|\gamma)\geq H(A_1\ldots A_n|\gamma)", "#44aaff", "Subadditivity"),
            ("Lemma 4", r"H(A|B)=H(A)\text{ (product)}", "#55ff99", "Product States"),
            ("Lemma 5", r"H(X|Y)\geq 0\text{ (class.)}", "#ff9800", "Positivity"),
            ("Lemma 6", r"H(\vec{a}|B\vec{x})\geq n-m", "#aa44ff", "IC Bound"),
        ]

        lem_boxes = VGroup()
        lem_texts = VGroup()
        for i, (name, eq, col, desc) in enumerate(lemmas_data):
            box = RoundedRectangle(color=col, fill_color="#0f0f1a", **lem_style)
            txt = VGroup(
                Text(name, font_size=18, color=col, weight=BOLD),
                MathTex(eq, font_size=14, color=GREY_B),
                Text(desc, font_size=12, color=GREY_D),
            ).arrange(DOWN, buff=0.08).move_to(box)
            lem_boxes.add(box)
            lem_texts.add(txt)
        lem_group = VGroup(*[VGroup(b, t) for b, t in zip(lem_boxes, lem_texts)])
        lem_group.arrange(RIGHT, buff=0.3).shift(UP*0.5)

        # ── Theorem box (bottom) ──
        thm_box = RoundedRectangle(corner_radius=0.15, width=8, height=1.6,
                                   color=YELLOW, fill_color="#2e2a0a",
                                   fill_opacity=0.9, stroke_width=3
                                   ).shift(DOWN*2)
        thm_text = VGroup(
            Text("Theorem 2", font_size=24, color=YELLOW, weight=BOLD),
            MathTex(r"\text{COND + SHAN + DPI} \;\Rightarrow\; \text{Tsirelson's Bound}",
                    font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.15).move_to(thm_box)

        # ── Connectors: axioms → lemmas (simple lines) ──
        axiom_lines = VGroup()
        connections = [
            (ax_cond, [0, 1, 2, 3]),
            (ax_shan, [1, 2, 3]),
            (ax_dpi, [0, 1, 2, 3]),
        ]
        for ax, targets in connections:
            for t in targets:
                line = Line(ax.get_bottom(), lem_boxes[t].get_top(),
                            color=GREY_D, stroke_width=1.5, buff=0.1)
                axiom_lines.add(line)

        # Connectors: lemmas → theorem
        lem_lines = VGroup()
        for lb in lem_boxes:
            line = Line(lb.get_bottom(), thm_box.get_top(),
                        color=YELLOW, stroke_width=2, buff=0.1,
                        stroke_opacity=0.7)
            lem_lines.add(line)

        # ============ ANIMATION ============
        # Axioms
        self.play(
            LaggedStart(
                AnimationGroup(Create(ax_cond), FadeIn(ax_cond_t)),
                AnimationGroup(Create(ax_shan), FadeIn(ax_shan_t)),
                AnimationGroup(Create(ax_dpi), FadeIn(ax_dpi_t)),
                lag_ratio=0.3
            ), run_time=1.5
        )
        self.wait(0.3)

        # Lines to lemmas
        self.play(LaggedStartMap(Create, axiom_lines, lag_ratio=0.05), run_time=1)

        # Lemmas one by one
        for i in range(4):
            self.play(Create(lem_boxes[i]), FadeIn(lem_texts[i]), run_time=0.6)
        self.wait(0.3)

        # Lines to theorem
        self.play(LaggedStartMap(Create, lem_lines, lag_ratio=0.1), run_time=0.8)

        # Theorem
        self.play(Create(thm_box), Write(thm_text), run_time=1)
        self.play(Indicate(thm_box, color=YELLOW, scale_factor=1.03), run_time=0.8)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene 2: LemmaDerivation  →  s3_lemma_flow.webm
# Step-by-step: H(a|Bx) >= n-m → IC → Tsirelson
# ─────────────────────────────────────────────────────────
class LemmaDerivation(Scene):
    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("From Axioms to Tsirelson", font_size=36, color=WHITE,
                     weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.7)

        # Step 1: Lemma 6 derivation
        step1_title = Text("Step 1: Bound on uncertainty", font_size=22,
                           color="#aa44ff", weight=BOLD).shift(UP*2.2 + LEFT*4)
        lines1 = VGroup(
            MathTex(r"H(\vec{a}|B\vec{x}) - H(\vec{x}|\vec{a}B) = H(\vec{a}) - H(\vec{x}|B)",
                    font_size=22, color=GREY_B),
            MathTex(r"\geq H(\vec{a}) - H(\vec{x})", font_size=22, color=GREY_B),
            MathTex(r"= n - H(\vec{x})", font_size=22, color=GREY_B),
            MathTex(r"\geq n - m", font_size=22, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(step1_title, DOWN, buff=0.2, aligned_edge=LEFT)

        labels1 = VGroup(
            Text("COND + product", font_size=12, color=GREY_D),
            Text("DPI: H(X|B) ≤ H(X)", font_size=12, color=GREY_D),
            Text("SHAN", font_size=12, color=GREY_D),
            Text("Shannon: H ≤ log", font_size=12, color=GREY_D),
        )
        for lbl, line in zip(labels1, lines1):
            lbl.next_to(line, RIGHT, buff=0.3)

        # Step 2: Subadditivity → per-bit bound
        step2_title = Text("Step 2: Split into individual bits", font_size=22,
                           color="#44aaff", weight=BOLD).shift(DOWN*0.2 + LEFT*4)
        lines2 = VGroup(
            MathTex(r"\sum_i H(a_i | B\vec{x}) \geq H(\vec{a}|B\vec{x}) \geq n - m",
                    font_size=22, color=GREY_B),
            MathTex(r"\sum_i H(a_i | \beta(i)) \geq n - m",
                    font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(step2_title, DOWN, buff=0.2, aligned_edge=LEFT)

        labels2 = VGroup(
            Text("Lemma 3 (subadditivity)", font_size=12, color=GREY_D),
            Text("DPI: β is function of B,x,i", font_size=12, color=GREY_D),
        )
        for lbl, line in zip(labels2, lines2):
            lbl.next_to(line, RIGHT, buff=0.3)

        # Step 3: → IC → Tsirelson
        step3_title = Text("Step 3: Recover IC", font_size=22,
                           color="#55ff99", weight=BOLD).shift(DOWN*2.0 + LEFT*4)
        lines3 = VGroup(
            MathTex(r"I = \sum_i I_{\text{Sh}}(a_i:\beta(i)) = n - \sum_i H(a_i|\beta(i)) \leq m",
                    font_size=22, color=GREY_B),
            MathTex(r"\Rightarrow \text{Tsirelson's bound: } S \leq 2\sqrt{2}",
                    font_size=24, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(step3_title, DOWN, buff=0.2, aligned_edge=LEFT)

        # ============ ANIMATION ============
        self.play(Write(step1_title), run_time=0.5)
        for i in range(4):
            self.play(Write(lines1[i]), FadeIn(labels1[i]), run_time=0.7)
        self.wait(0.5)

        self.play(Write(step2_title), run_time=0.5)
        for i in range(2):
            self.play(Write(lines2[i]), FadeIn(labels2[i]), run_time=0.7)
        self.wait(0.5)

        self.play(Write(step3_title), run_time=0.5)
        self.play(Write(lines3[0]), run_time=0.8)
        self.play(Write(lines3[1]), run_time=0.8)
        self.play(Circumscribe(lines3[1], color=YELLOW, buff=0.1), run_time=0.8)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene 3: BoxWorldBreaks  →  s3_boxworld.webm
# Shows box-world violating DPI and Strong Subadditivity
# ─────────────────────────────────────────────────────────
class BoxWorldBreaks(Scene):
    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("Where Box-World Breaks Down", font_size=36, color="#ff5555",
                     weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.7)

        # Two columns
        # Left: What QM satisfies
        qm_title = Text("Quantum Mechanics", font_size=22, color="#aa44ff",
                        weight=BOLD).shift(LEFT*4 + UP*2)
        qm_items = VGroup(
            VGroup(MathTex(r"\checkmark", font_size=22, color=GREEN),
                   Text("DPI holds", font_size=18, color=GREY_B)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\checkmark", font_size=22, color=GREEN),
                   Text("Strong subadditivity", font_size=18, color=GREY_B)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\checkmark", font_size=22, color=GREEN),
                   Text("H(X|Y) ≥ 0 (classical)", font_size=18, color=GREY_B)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\checkmark", font_size=22, color=GREEN),
                   Text("IC: I ≤ m", font_size=18, color=GREY_B)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\checkmark", font_size=22, color=GREEN),
                   MathTex(r"S \leq 2\sqrt{2}", font_size=18, color=GREY_B)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(qm_title, DOWN, buff=0.3, aligned_edge=LEFT)

        # Right: What box-world violates
        bw_title = Text("Box-World", font_size=22, color="#ff5555",
                        weight=BOLD).shift(RIGHT*3 + UP*2)
        bw_items = VGroup(
            VGroup(MathTex(r"\times", font_size=22, color="#ff5555"),
                   Text("DPI violated!", font_size=18, color="#ff5555")).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\times", font_size=22, color="#ff5555"),
                   Text("SSA violated!", font_size=18, color="#ff5555")).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\times", font_size=22, color="#ff5555"),
                   Text("Conditional entropy < 0", font_size=18, color="#ff5555")).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\times", font_size=22, color="#ff5555"),
                   Text("IC violated: I > m", font_size=18, color="#ff5555")).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"\times", font_size=22, color="#ff5555"),
                   MathTex(r"S = 4 > 2\sqrt{2}", font_size=18, color="#ff5555")).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(bw_title, DOWN, buff=0.3, aligned_edge=LEFT)

        # Divider
        divider = DashedLine(UP*2.2, DOWN*1.5, color=GREY_D, stroke_width=1.5,
                             dash_length=0.1).shift(DOWN*0.3)

        # Conclusion box
        conclusion = RoundedRectangle(corner_radius=0.12, width=10, height=1.4,
                                      color=YELLOW, fill_color="#2e2a0a",
                                      fill_opacity=0.8, stroke_width=2
                                      ).shift(DOWN*2.8)
        conc_text = VGroup(
            Text("DPI is the dividing line!", font_size=22, color=YELLOW, weight=BOLD),
            Text("Any theory violating DPI can exceed Tsirelson's bound",
                 font_size=16, color=GREY_B),
        ).arrange(DOWN, buff=0.1).move_to(conclusion)

        # ============ ANIMATION ============
        self.play(Write(qm_title), Write(bw_title), Create(divider), run_time=0.8)

        # Animate row by row, side by side
        for i in range(5):
            self.play(FadeIn(qm_items[i]), FadeIn(bw_items[i]), run_time=0.6)
            self.wait(0.2)

        self.wait(0.3)
        self.play(Create(conclusion), Write(conc_text), run_time=1)
        self.play(Indicate(conclusion, color=YELLOW, scale_factor=1.02), run_time=0.8)

        self.wait(2)


# ─────────────────────────────────────────────────────────
# Scene 4: BigPicture  →  s3_big_picture.webm
# Zooms out to show the broader landscape: what was achieved
# and open questions.
# ─────────────────────────────────────────────────────────
class BigPicture(Scene):
    def construct(self):
        self.camera.background_color = "#0f0f1a"

        title = Text("The Big Picture", font_size=38, color=WHITE,
                     weight=BOLD).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.7)

        # ── Concentric circles representing theory hierarchy ──
        center = ORIGIN
        circles = VGroup()
        circle_data = [
            (3.5, "#ff444440", "#ff4444", "No-Signaling"),
            (2.5, "#aa44ff30", "#aa44ff", "Quantum"),
            (1.5, "#44aaff30", "#44aaff", "Classical"),
        ]
        labels = VGroup()
        for r, fill, stroke, name in circle_data:
            c = Circle(radius=r, color=stroke, fill_color=fill,
                       fill_opacity=0.15, stroke_width=2.5).move_to(center)
            circles.add(c)
            lbl = Text(name, font_size=18, color=stroke, weight=BOLD
                       ).move_to(center + UP*(r - 0.25))
            labels.add(lbl)

        # ── What rules each boundary ──
        annotations = VGroup()
        # Classical boundary
        ann1 = VGroup(
            Line(center + RIGHT*1.5 + DOWN*0.3, center + RIGHT*4.5 + DOWN*0.3,
                 color="#44aaff", stroke_width=1.5),
            Text("Bell inequalities", font_size=14, color="#44aaff"
                 ).move_to(center + RIGHT*5.5 + DOWN*0.3),
        )
        # Quantum boundary
        ann2 = VGroup(
            Line(center + RIGHT*2.5 + DOWN*0.8, center + RIGHT*4.5 + DOWN*0.8,
                 color="#aa44ff", stroke_width=1.5),
            VGroup(
                Text("DPI → IC → Tsirelson", font_size=14, color="#aa44ff"),
                Text("(This paper!)", font_size=12, color=YELLOW),
            ).arrange(DOWN, buff=0.05).move_to(center + RIGHT*5.8 + DOWN*0.9),
        )
        # NS boundary
        ann3 = VGroup(
            Line(center + RIGHT*3.5 + DOWN*1.3, center + RIGHT*4.5 + DOWN*1.3,
                 color="#ff4444", stroke_width=1.5),
            Text("Relativity (no-signaling)", font_size=14, color="#ff4444"
                 ).move_to(center + RIGHT*5.9 + DOWN*1.3),
        )
        annotations.add(ann1, ann2, ann3)

        # ── PR-Box dot outside quantum but inside NS ──
        pr_dot = Dot(center + 3.0*np.array([np.cos(-30*DEGREES),
                                             np.sin(-30*DEGREES), 0]),
                     color="#ff5555", radius=0.12, z_index=5)
        pr_label = Text("PR-Box", font_size=14, color="#ff5555"
                        ).next_to(pr_dot, DOWN+RIGHT, buff=0.1)
        # X through PR-box
        pr_cross = Cross(stroke_color="#ff5555", stroke_width=3
                         ).scale(0.2).move_to(pr_dot)

        # ── Open questions (bottom) ──
        oq_box = RoundedRectangle(corner_radius=0.1, width=10.5, height=1.4,
                                  color=GREY_D, fill_color="#12122a",
                                  fill_opacity=0.9, stroke_width=1.5
                                  ).to_edge(DOWN, buff=0.3)
        oq_title = Text("Open Questions", font_size=18, color=YELLOW,
                        weight=BOLD).move_to(oq_box.get_center() + UP*0.3)
        oq_items = VGroup(
            Text("Can DPI + additional axioms fully derive quantum theory?",
                 font_size=14, color=GREY_B),
            Text("Are there non-quantum theories between Classical & Tsirelson that satisfy DPI?",
                 font_size=14, color=GREY_B),
        ).arrange(RIGHT, buff=1.5).move_to(oq_box.get_center() + DOWN*0.2)

        # ============ ANIMATION ============
        # Draw circles from outside in
        for i in range(3):
            self.play(Create(circles[i]), Write(labels[i]), run_time=0.6)
        self.wait(0.3)

        # Annotations
        for ann in annotations:
            self.play(FadeIn(ann), run_time=0.6)

        # PR-Box
        self.play(FadeIn(pr_dot), Write(pr_label), run_time=0.5)
        self.play(Create(pr_cross), run_time=0.5)
        self.wait(0.3)

        # Open questions
        self.play(Create(oq_box), Write(oq_title), run_time=0.7)
        self.play(FadeIn(oq_items), run_time=0.8)

        self.wait(2)
