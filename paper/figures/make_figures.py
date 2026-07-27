"""Generate the five manuscript figures from numbers already in the tables (no new
data). Colors come from the dataviz skill's validated reference palette (sequential
blue ramp for magnitude; categorical hues for series) -- not hand-picked hex values.

Figures, in manuscript order:
  fig1_pipeline.png           research-stage flowchart          (Section 2)
  fig2_taxonomy.png           register-pragmatic taxonomy       (Section 2.3)
  fig3_validator_bars.png     authenticity by generator/rater   (Section 3.4)
  fig4_detection_heatmap.png  detection rate heatmap            (Section 3.5)
  fig5_detection_ci.png       detection rate with Wilson CIs    (Section 3.5)

Figures 1 and 5 were added in the JUTIF R1 revision (Reviewer A comment 4 /
Reviewer B comments 9 and 13). Output is 400 dpi: the journal requires more than
300 dpi, and the previous 300-dpi setting rendered as 299.9994.

Run: python paper/figures/make_figures.py
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

DPI = 400

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "sans-serif"]

INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"
CATEGORICAL_ORANGE = "#eb6834"   # slot 8 -- ngoko (hot/direct) tint
SEQ_BLUE_LIGHT = "#b7d3f6"       # sequential step 150 -- krama (cool) tint

# sequential blue ramp (palette.md), steps 100..700, used for the heatmap
SEQ_STOPS = [
    (0.00, "#f4f8fe"),   # slightly lighter than step 100, lets 0% recede to white
    (0.15, "#cde2fb"),   # 100
    (0.30, "#9ec5f4"),   # 200
    (0.45, "#6da7ec"),   # 300
    (0.60, "#3987e5"),   # 400
    (0.75, "#1c5cab"),   # 550
    (1.00, "#0d366b"),   # 700
]
SEQ_CMAP = LinearSegmentedColormap.from_list("seq_blue", SEQ_STOPS)


def fig2_taxonomy():
    fig, ax = plt.subplots(figsize=(7.0, 2.5), dpi=DPI)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1.42)
    ax.axis("off")

    niches = [
        dict(code="N1", name="ngoko direct", register="ngoko", fill=CATEGORICAL_ORANGE,
             mode="Hot, open aggression", mech="Explicit slur + profanity\nto addressee or about group"),
        dict(code="N2", name="krama report", register="krama", fill=SEQ_BLUE_LIGHT,
             mode="Derogatory report,\nabsent target", mech='Polite prayer/concern framing\nderogates a third party'),
        dict(code="N3a", name="krama sarcastic", register="krama", fill=SEQ_BLUE_LIGHT,
             mode="Ironic over-praise\n(pasemon)", mech="Mock-deference:\nweaponized honorifics"),
        dict(code="N3b", name="krama cold contempt", register="krama", fill=SEQ_BLUE_LIGHT,
             mode="Moral/hierarchical\nsuperiority", mech="Cold indictment: target lacks\nisin or unggah-ungguh"),
    ]

    box_w, gap = 0.88, 0.12
    for i, n in enumerate(niches):
        x0 = i * (box_w + gap) + 0.06
        alpha = 0.30 if n["register"] == "ngoko" else 0.45
        box = FancyBboxPatch((x0, 0.08), box_w, 1.30, boxstyle="round,pad=0.02,rounding_size=0.04",
                              linewidth=1.1, edgecolor=INK, facecolor=n["fill"], alpha=alpha,
                              transform=ax.transData)
        box.set_alpha(alpha)
        ax.add_patch(box)
        cx = x0 + box_w / 2
        ax.text(cx, 1.28, n["code"], ha="center", va="top", fontsize=13, fontweight="bold", color=INK)
        ax.text(cx, 1.11, n["name"], ha="center", va="top", fontsize=8.3, style="italic", color=INK)
        ax.text(cx, 0.90, n["mode"], ha="center", va="top", fontsize=7.6, color=INK, linespacing=1.4)
        ax.text(cx, 0.52, n["mech"], ha="center", va="top", fontsize=7.0, color=MUTED, linespacing=1.4)

    # register legend strip
    ax.add_patch(plt.Rectangle((0.06, -0.12), box_w, 0.12, facecolor=CATEGORICAL_ORANGE, alpha=0.30,
                                edgecolor="none", clip_on=False))
    ax.text(0.06 + box_w / 2, -0.06, "ngoko (hot)", ha="center", va="center", fontsize=7.2, color=INK, clip_on=False)
    krama_x0 = 1 * (box_w + gap) + 0.06
    krama_w = 3 * box_w + 2 * gap
    ax.add_patch(plt.Rectangle((krama_x0, -0.12), krama_w, 0.12, facecolor=SEQ_BLUE_LIGHT, alpha=0.45,
                                edgecolor="none", clip_on=False))
    ax.text(krama_x0 + krama_w / 2, -0.06, "krama (cool)", ha="center", va="center", fontsize=7.2, color=INK, clip_on=False)

    fig.tight_layout(rect=[0, 0.02, 1, 0.98])
    fig.savefig("paper/figures/fig2_taxonomy.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig4_heatmap():
    niches = ["N1 ngoko\ndirect", "N2 krama\nreport", "N3a krama\nsarcastic", "N3b krama\ncold contempt"]
    detectors = ["DeepSeek", "Grok", "Qwen3-14B", "Gemma3-27B", "GPT-OSS-20B"]
    data = np.array([
        [100, 100, 100, 100, 100],
        [78, 89, 44, 89, 44],
        [11, 11, 0, 0, 0],
        [78, 89, 56, 78, 78],
    ], dtype=float)

    fig, ax = plt.subplots(figsize=(6.2, 3.4), dpi=DPI)
    im = ax.imshow(data, cmap=SEQ_CMAP, vmin=0, vmax=100, aspect="auto")

    ax.set_xticks(range(len(detectors)))
    ax.set_xticklabels(detectors, fontsize=8, color=INK)
    ax.set_yticks(range(len(niches)))
    ax.set_yticklabels(niches, fontsize=8, color=INK)
    ax.tick_params(length=0)

    # 2px surface-colored gaps between cells
    ax.set_xticks(np.arange(-0.5, len(detectors), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(niches), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=3)
    ax.tick_params(which="minor", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            v = data[i, j]
            txt_color = "white" if v >= 55 else INK
            ax.text(j, i, f"{int(v)}%", ha="center", va="center", fontsize=9,
                     color=txt_color, fontweight="bold" if v <= 11 else "normal")

    # highlight the blind-spot row (N3a) with an accent outline, not a color change
    ax.add_patch(plt.Rectangle((-0.5, 1.5), len(detectors), 1, fill=False,
                                edgecolor="#e34948", linewidth=2.2, zorder=5))

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("detection rate (% cells flagged hate)", fontsize=7.5, color=MUTED)
    cbar.ax.tick_params(labelsize=7, length=0)

    fig.tight_layout()
    fig.savefig("paper/figures/fig4_detection_heatmap.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig3_validator_bars():
    generators = ["DeepSeek", "Gemma3-27B", "Qwen3-14B"]
    validators = ["Mukhlis", "Yekti", "Daniel"]
    data = {
        "Mukhlis": [97, 56, 11],
        "Yekti": [100, 97, 75],
        "Daniel": [97, 39, 0],
    }
    colors = {
        "Mukhlis": "#2a78d6",
        "Yekti": "#1baf7a",
        "Daniel": "#eda100",
    }

    fig, ax = plt.subplots(figsize=(6.4, 2.8), dpi=DPI)

    n_series = len(validators)
    bar_w = 0.24
    group_gap = 0.12  # extra space between the 3-bar clusters
    x = np.arange(len(generators)) * (n_series * bar_w + group_gap)

    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID, linewidth=0.9, zorder=0)
    ax.xaxis.grid(False)

    for i, v in enumerate(validators):
        offset = (i - (n_series - 1) / 2) * bar_w
        vals = data[v]
        bars = ax.bar(x + offset, vals, width=bar_w * 0.92, color=colors[v],
                       edgecolor="white", linewidth=0.8, label=v, zorder=3)
        for rect, val in zip(bars, vals):
            y = val if val > 0 else 0
            va = "bottom"
            y_label = y + 2
            ax.text(rect.get_x() + rect.get_width() / 2, y_label, f"{val}%",
                     ha="center", va=va, fontsize=7, color=INK)

    ax.set_xticks(x)
    ax.set_xticklabels(generators, fontsize=8, color=INK, rotation=0)
    ax.set_ylim(0, 105)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=8, color=INK)
    ax.tick_params(length=0)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)

    ax.legend(fontsize=7.5, frameon=False, loc="upper right",
              bbox_to_anchor=(1.0, 1.02), ncol=1, handlelength=1.2, handletextpad=0.5)

    fig.tight_layout()
    fig.savefig("paper/figures/fig3_validator_bars.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig1_pipeline():
    """Research-stage flowchart: filtering -> labeling baseline -> stimulus
    construction -> native validation -> detector probe."""
    stages = [
        dict(title="1. Corpus\nfiltering",
             body="Public Indonesian\nhate-speech dump\n(12,700 tweets)\n"
                  "LLM Javanese filter\n→ 735 in-scope texts",
             fill=SEQ_BLUE_LIGHT),
        dict(title="2. Labeling\nbaseline",
             body="3 LLM raters,\ncultural prompt\n→ 728 consensus labels\n"
                  "zero krama-hate\n(scarcity established)",
             fill=SEQ_BLUE_LIGHT),
        dict(title="3. Stimulus\nconstruction",
             body="4 niches × 9 targets\n= 36-cell matrix\n3 generator models\n"
                  "→ 108 examples",
             fill=CATEGORICAL_ORANGE),
        dict(title="4. Native\nvalidation",
             body="3 raters, independent\nand blind\nauthenticity +\n"
                  "clearly-hate judgment",
             fill=CATEGORICAL_ORANGE),
        dict(title="5. Detection\nprobe",
             body="36 cells ×\n5 detector models\n→ 180 verdicts\n"
                  "detection rate per niche",
             fill=CATEGORICAL_ORANGE),
    ]

    box_w, box_h, gap, pad = 1.92, 1.50, 0.30, 0.06
    total_w = len(stages) * box_w + (len(stages) - 1) * gap + 2 * pad

    fig, ax = plt.subplots(figsize=(7.4, 1.95), dpi=DPI)
    ax.set_xlim(0, total_w)
    ax.set_ylim(0, box_h + 0.52)
    ax.axis("off")

    y0 = 0.40
    for i, s in enumerate(stages):
        x0 = pad + i * (box_w + gap)
        ax.add_patch(FancyBboxPatch(
            (x0, y0), box_w, box_h,
            boxstyle="round,pad=0.015,rounding_size=0.05",
            linewidth=1.1, edgecolor=INK, facecolor=s["fill"], alpha=0.32))
        cx = x0 + box_w / 2
        ax.text(cx, y0 + box_h - 0.10, s["title"], ha="center", va="top",
                fontsize=7.4, fontweight="bold", color=INK, linespacing=1.3)
        ax.text(cx, y0 + box_h - 0.62, s["body"], ha="center", va="top",
                fontsize=6.3, color=INK, linespacing=1.55)

        if i < len(stages) - 1:
            ax.add_patch(FancyArrowPatch(
                (x0 + box_w + 0.02, y0 + box_h / 2),
                (x0 + box_w + gap - 0.02, y0 + box_h / 2),
                arrowstyle="-|>", mutation_scale=9, linewidth=1.1,
                color=MUTED, shrinkA=0, shrinkB=0))

    # phase strip: which stages establish the problem vs. measure it
    strip_a_w = 2 * box_w + gap
    ax.add_patch(plt.Rectangle((pad, 0.10), strip_a_w, 0.17,
                               facecolor=SEQ_BLUE_LIGHT, alpha=0.55, edgecolor="none"))
    ax.text(pad + strip_a_w / 2, 0.185, "establishes the collection paradox",
            ha="center", va="center", fontsize=6.4, color=INK)
    x_probe = pad + 2 * (box_w + gap)
    strip_b_w = 3 * box_w + 2 * gap
    ax.add_patch(plt.Rectangle((x_probe, 0.10), strip_b_w, 0.17,
                               facecolor=CATEGORICAL_ORANGE, alpha=0.32, edgecolor="none"))
    ax.text(x_probe + strip_b_w / 2, 0.185, "constructs and measures the blind spot",
            ha="center", va="center", fontsize=6.4, color=INK)

    fig.tight_layout()
    fig.savefig("paper/figures/fig1_pipeline.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return max(0.0, c - h), min(1.0, c + h)


def fig5_detection_ci():
    """Grouped bars with Wilson 95% intervals -- the interval companion to the
    heatmap, added so the small per-cell sample size is visible in the figure."""
    with open("experiments/generation_pilot/detect_counts_aggregate.json",
              encoding="utf-8") as fh:
        agg = json.load(fh)

    niches = ["ngoko_direct", "krama_report", "krama_sarcastic", "krama_cold_contempt"]
    labels = ["N1 ngoko\ndirect", "N2 krama\nreport", "N3a krama\nsarcastic",
              "N3b krama\ncold contempt"]
    detectors = ["deepseek", "grok", "qwen3:14b", "gemma3:27b", "gpt-oss:20b"]
    disp = ["DeepSeek", "Grok", "Qwen3-14B", "Gemma3-27B", "GPT-OSS-20B"]
    colors = ["#2a78d6", "#1baf7a", "#eda100", "#eb6834", "#8a63d2"]

    fig, ax = plt.subplots(figsize=(7.0, 3.0), dpi=DPI)
    n_series = len(detectors)
    bar_w = 0.15
    x = np.arange(len(niches)) * (n_series * bar_w + 0.22)

    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID, linewidth=0.9, zorder=0)

    for i, (d, name) in enumerate(zip(detectors, disp)):
        offset = (i - (n_series - 1) / 2) * bar_w
        vals, los, his = [], [], []
        for niche in niches:
            c = agg[niche][d]
            k, n = c["hate"], c["total"]
            lo, hi = _wilson(k, n)
            vals.append(100 * k / n)
            los.append(100 * k / n - 100 * lo)
            his.append(100 * hi - 100 * k / n)
        ax.bar(x + offset, vals, width=bar_w * 0.9, color=colors[i],
               edgecolor="white", linewidth=0.6, label=name, zorder=3)
        ax.errorbar(x + offset, vals, yerr=[los, his], fmt="none",
                    ecolor=MUTED, elinewidth=0.8, capsize=1.8, zorder=4)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=7.6, color=INK)
    ax.set_ylim(0, 112)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=7.6, color=INK)
    ax.set_ylabel("detection rate", fontsize=8, color=MUTED)
    ax.tick_params(length=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.legend(fontsize=6.8, frameon=False, ncol=5, loc="upper center",
              bbox_to_anchor=(0.5, 1.14), handlelength=1.1, handletextpad=0.4,
              columnspacing=1.2)

    fig.tight_layout()
    fig.savefig("paper/figures/fig5_detection_ci.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig1_pipeline()
    fig2_taxonomy()
    fig3_validator_bars()
    fig4_heatmap()
    fig5_detection_ci()
    print("Wrote fig1_pipeline.png, fig2_taxonomy.png, fig3_validator_bars.png, "
          "fig4_detection_heatmap.png, fig5_detection_ci.png (400 dpi)")
