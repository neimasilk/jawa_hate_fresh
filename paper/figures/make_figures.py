"""Generate Fig. 1 (register-pragmatic taxonomy diagram) and Fig. 2 (detection-rate
heatmap) for draft_jinita.md, from the numbers already in Table 3/Table 4 (no new
data). Colors come from the dataviz skill's validated reference palette
(sequential blue ramp for magnitude; categorical orange/blue at reduced alpha for
the two-register distinction) -- not hand-picked hex values.

Run: python paper/figures/make_figures.py
Writes: fig1_taxonomy.png, fig2_detection_heatmap.png (300 dpi, print-safe)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

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


def fig1_taxonomy():
    fig, ax = plt.subplots(figsize=(7.0, 2.5), dpi=300)
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
    fig.savefig("paper/figures/fig1_taxonomy.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2_heatmap():
    niches = ["N1 ngoko\ndirect", "N2 krama\nreport", "N3a krama\nsarcastic", "N3b krama\ncold contempt"]
    detectors = ["DeepSeek", "Grok", "Qwen3-14B", "Gemma3-27B", "GPT-OSS-20B"]
    data = np.array([
        [100, 100, 100, 100, 100],
        [78, 89, 44, 89, 44],
        [11, 11, 0, 0, 0],
        [78, 89, 56, 78, 78],
    ], dtype=float)

    fig, ax = plt.subplots(figsize=(6.2, 3.4), dpi=300)
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
    fig.savefig("paper/figures/fig2_detection_heatmap.png", bbox_inches="tight", facecolor="white")
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

    fig, ax = plt.subplots(figsize=(6.4, 2.8), dpi=300)

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


if __name__ == "__main__":
    fig1_taxonomy()
    fig2_heatmap()
    fig3_validator_bars()
    print("Wrote paper/figures/fig1_taxonomy.png, fig2_detection_heatmap.png, "
          "and fig3_validator_bars.png")
