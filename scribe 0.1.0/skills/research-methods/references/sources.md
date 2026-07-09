# Sources — prior art behind each method

Provenance for the six method protocols. Each method is an established technique from optimization,
debugging, experimental methodology, or QA — not invented here. Cited 2026-07-04 at authoring; verify
against the primary source before treating any detail as canonical (the protocols adapt these to a
scorer-driven agent loop, they do not reproduce them verbatim).

| Method | Grounded in | Reference |
|---|---|---|
| **Autoresearch** | Andrej Karpathy's "autoresearch" pattern — let an agent run experiments autonomously, keeping only changes that improve a measured score, one change per round with a changelog. | Karpathy, public talks/notes on autonomous experiment loops (e.g. the nanoGPT / "let it cook" workflow). |
| **Ablation** | Ablation study — the standard experimental-methodology technique of removing one component at a time to measure its contribution, ubiquitous in ML papers' ablation sections. | Experimental methodology; ML ablation-study convention (Meyes et al., "Ablation Studies in Artificial Neural Networks," 2019, arXiv:1901.08644). |
| **Bisect** | Binary search for a fault-introducing change — logarithmic root-cause isolation over an ordered change history. | `git-bisect(1)`, Git documentation (git-scm.com/docs/git-bisect); classic binary-search debugging. |
| **Adversarial** | Adversarial / negative testing — attack the system with inputs designed to fail it; boundary analysis, fuzzing, and property-based testing. | OWASP Testing Guide (owasp.org); Claessen & Hughes, "QuickCheck" (ICFP 2000) for property-based testing; fuzzing literature. |
| **Hill Climb** | Hill-climbing local search — evaluate the neighborhood, move to the best neighbor, repeat until no neighbor improves; stop at a local optimum. | Russell & Norvig, *Artificial Intelligence: A Modern Approach*, local-search chapter (hill-climbing). |
| **Sweep** | Parameter sweep / grid search over a value range to map the scoring landscape and read sensitivity; the "narrow the range first" discipline. | Hyperparameter-optimization practice; Bergstra & Bengio, "Random Search for Hyper-Parameter Optimization" (JMLR 2012) for the grid-vs-range trade-off. |

**Adding or re-homing a method** is authoring work — route to [[knowledge-forge]] (axis decomposition,
a grounded research wave, index discipline). A new method lands with its citation added here, never as an
uncited protocol bolted on inline.
