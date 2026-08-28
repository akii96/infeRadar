# AITER: PR digest (2026-08-23 to 2026-08-27)

_77 merged, 63 newly opened - source ROCm/AITER, generated 2026-08-27T19:30:18Z_

## TL;DR
- **DeepSeek-V4** dominated development this cycle, alongside notable attention for Kimi, GLM, and Qwen. The primary focus was on needle-moving performance work for AMD's **gfx1250** and **gfx950** architectures.
- **Attention & MLA:** Significant advancements in Multi-Head Latent Attention (MLA), including sparse MLA training backward and new prebuilt OPUS kernels for sparse paged prefill on gfx1250.
- **Quantization & MoE:** Heavy investment in low-precision primitives, particularly MXFP8/MXFP4 and A8W8 blockscale quantization for GEMMs and MoE, coupled with a massive cleanup of legacy Triton/Gluon MoE code.
- **Framework & Architecture:** A major architectural shift is underway to unify OPUS GEMM/BMM interfaces with PyTorch workspaces, alongside the massive in-progress "Lumen" development branch targeting comprehensive Triton/Gluon/HIP optimizations.

## Most important PRs
- **[#4903](https://github.com/ROCm/aiter/pull/4903)** Integrates OPUS BF16 GEMM co-processor support via JIT compilation. This merged PR is a massive architectural addition for gfx1250, paving the way for significant DeepSeek performance wins.
- **[#4978](https://github.com/ROCm/aiter/pull/4978)** Introduces "Lumen", a massive newly-opened development branch spanning Triton, Gluon, and HIP. It touches almost every critical path (attention, MLA, MoE, quantization) specifically targeting DeepSeek on gfx942.
- **[#4833](https://github.com/ROCm/aiter/pull/4833)** Deletes over 9,000 lines of legacy Triton/Gluon MoE code. This merged cleanup aggressively standardizes the MoE routing and quantization paths across AMD architectures.
- **[#4773](https://github.com/ROCm/aiter/pull/4773)** Implements MXFP8 GEMM kernels in Triton/Gluon for gfx1250. This merged work provides a critical low-precision performance primitive for DeepSeek and other models.
- **[#4961](https://github.com/ROCm/aiter/pull/4961)** Unifies OPUS GEMM and BMM interfaces to use PyTorch workspaces. This newly-opened refactor standardizes memory management for custom OPUS kernels across all recent AMD architectures.

## More changes by area

<details>
<summary>Kernels & attention (27)</summary>

- [#4869](https://github.com/ROCm/aiter/pull/4869) Optimize conv2d for RDNA - kernels, routing, and input packing
- [#4281](https://github.com/ROCm/aiter/pull/4281) Add TDM deep-prefetch BF16 prefill for qk_norm_rope on gfx1250
- [#4748](https://github.com/ROCm/aiter/pull/4748) Fix asm gemm: add a_preshuffle=0 f4gemm & f8gemm, fix corner case support
- [#4766](https://github.com/ROCm/aiter/pull/4766) Sparse MLA training backward for GFX950/DSV4
- [#4803](https://github.com/ROCm/aiter/pull/4803) fused_clamp_act_mul gluon kernel
- [#4967](https://github.com/ROCm/aiter/pull/4967) MHA v4: support GQA, add gfx950 bf16, add gfx942 i8/fp8
- [#4877](https://github.com/ROCm/aiter/pull/4877) OPUS MHA Support LSE on GFX950
- [#5012](https://github.com/ROCm/aiter/pull/5012) DSv4 sparse paged prefill attention via prebuilt OPUS kernels on gfx1250
- [#4726](https://github.com/ROCm/aiter/pull/4726) Fuse block-banking cat into attn_res_gate
- [#5024](https://github.com/ROCm/aiter/pull/5024) Add MHA forward tuning scripts and kernel-info dumping
- [#5023](https://github.com/ROCm/aiter/pull/5023) Consolidate and reorganize ops/triton utils
- [#5005](https://github.com/ROCm/aiter/pull/5005) Block-sparse MHAv4 with load-balancing
- [#4992](https://github.com/ROCm/aiter/pull/4992) gfx950 hd=72 varlen FMHA for Qwen3-VL prefill
- [#4926](https://github.com/ROCm/aiter/pull/4926) add mla v4 prefill asm kernel
- [#5046](https://github.com/ROCm/aiter/pull/5046) fp8_mqa_logits: hand-written gfx950 prefill indexer kernel
- [#5047](https://github.com/ROCm/aiter/pull/5047) fp8_paged_mqa_logits: hand-written gfx950 decode indexer kernel
- [#5048](https://github.com/ROCm/aiter/pull/5048) add an optimized prefill fp8_mqa_logits for H64D128
- [#4968](https://github.com/ROCm/aiter/pull/4968) Support Q/K D192 with asymmetric K/V head dim
- [#4958](https://github.com/ROCm/aiter/pull/4958) Make aiter_opus_plus.h torch-free + Cluster A + mha_v4_quant
- [#4971](https://github.com/ROCm/aiter/pull/4971) gfx950 hd256 FP8 LINEAR paged-varlen asm prefill
- [#5043](https://github.com/ROCm/aiter/pull/5043) asm mha bf16 hd192x128
- [#5010](https://github.com/ROCm/aiter/pull/5010) Support caller-defined padding cache slot in fused MLA writer
- [#4966](https://github.com/ROCm/aiter/pull/4966) Prevent duplicate JIT tracing on concurrent kernel startup
- [#5002](https://github.com/ROCm/aiter/pull/5002) Add Qwen3 Next FP8 QKV preparation
- [#4976](https://github.com/ROCm/aiter/pull/4976) select sink kernel when only sink_ptr is provided
- [#5025](https://github.com/ROCm/aiter/pull/5025) jdbmm backward pass
- [#5011](https://github.com/ROCm/aiter/pull/5011) Add TopK

</details>

<details>
<summary>MoE & quantization (30)</summary>

- [#4850](https://github.com/ROCm/aiter/pull/4850) gradlib gemm + moe_mxfp4_aux + mha_native_splitkv + custom_all_reduce_gfx1250
- [#4866](https://github.com/ROCm/aiter/pull/4866) Move gluon gemm_a8w8 kernel into _gluon_kernels/gfx950
- [#4906](https://github.com/ROCm/aiter/pull/4906) update gfx950 layout fmoe2 csv
- [#4917](https://github.com/ROCm/aiter/pull/4917) Move gluon gemm_a8w8_blockscale kernel into _gluon_kernels
- [#4965](https://github.com/ROCm/aiter/pull/4965) topk_gating: fix dropped and out-of-range top-k slots
- [#4049](https://github.com/ROCm/aiter/pull/4049) Gluon Fused Dynamic mxfp4 Quant Moe Sort for gfx1250
- [#4960](https://github.com/ROCm/aiter/pull/4960) update shuffle
- [#4955](https://github.com/ROCm/aiter/pull/4955) Force fp4gemm preshuffle to triton on gfx1250
- [#4620](https://github.com/ROCm/aiter/pull/4620) Added Gelu with tanh approx for CK XDL 2-stage MoE
- [#4954](https://github.com/ROCm/aiter/pull/4954) MXFP8 activation passthrough in fused_moe
- [#5037](https://github.com/ROCm/aiter/pull/5037) MOE a8w4 cudagraph updates
- [#5017](https://github.com/ROCm/aiter/pull/5017) gfx942 a16wi4: pack f32->bf16 with lshr-16 instead of scalar
- [#4995](https://github.com/ROCm/aiter/pull/4995) add missing XQ scale barrier in a16 FP8-blockscale kernels
- [#5015](https://github.com/ROCm/aiter/pull/5015) fused_moe: require GUGU gu_interleave layout
- [#4951](https://github.com/ROCm/aiter/pull/4951) add mxfp8 a8w8 blockscale for gfx950
- [#5001](https://github.com/ROCm/aiter/pull/5001) optimize fused stage1 and AOT bundles for mega_moe
- [#4980](https://github.com/ROCm/aiter/pull/4980) A4W4 mega_moe operator
- [#4991](https://github.com/ROCm/aiter/pull/4991) Fix inverse rope group quant gfx1250
- [#4970](https://github.com/ROCm/aiter/pull/4970) QRInt4: INT4 two-shot all-reduce for gfx942/gfx950
- [#4997](https://github.com/ROCm/aiter/pull/4997) Move fp4 GEMM gluon to _gluon_kernels
- [#4984](https://github.com/ROCm/aiter/pull/4984) quantize before dispatch, on an fp8 or fp4 wire for mega_moe/gfx1250
- [#5009](https://github.com/ROCm/aiter/pull/5009) Radix-select top-k for wide ungrouped MoE routers
- [#5041](https://github.com/ROCm/aiter/pull/5041) Add batched a8w8 mxscale_128 gemm
- [#5007](https://github.com/ROCm/aiter/pull/5007) One-stage split-K for the a8w8 preshuffle GEMM
- [#5029](https://github.com/ROCm/aiter/pull/5029) Add bench for gluon/triton mxfp8 gemm
- [#5052](https://github.com/ROCm/aiter/pull/5052) Support a4w4 in test_mega_moe
- [#5038](https://github.com/ROCm/aiter/pull/5038) Moe routing optimizations
- [#5058](https://github.com/ROCm/aiter/pull/5058) Keep forced MXFP4 FlyDSL routing opt-in
- [#5055](https://github.com/ROCm/aiter/pull/5055) mxfp8 gemm cga update
- [#5053](https://github.com/ROCm/aiter/pull/5053) combine routing early exit

</details>

<details>
<summary>Parallelism & scheduling (5)</summary>

- [#4985](https://github.com/ROCm/aiter/pull/4985) comm fused moe
- [#4981](https://github.com/ROCm/aiter/pull/4981) mega all gather merge stage1
- [#4977](https://github.com/ROCm/aiter/pull/4977) Single-kernel Lamport fused all-reduce + RMSNorm (opt-in)
- [#4990](https://github.com/ROCm/aiter/pull/4990) Widen the AR+RMSNorm reduce-scatter producer
- [#4924](https://github.com/ROCm/aiter/pull/4924) make raw IPC input pools usable — remove init_dist_env's vestigial signal/buffer block

</details>

<details>
<summary>Performance (41)</summary>

- [#4554](https://github.com/ROCm/aiter/pull/4554) configs: add tuned configs for Qwen3-VL-235B MXFP4 (gfx950)
- [#4453](https://github.com/ROCm/aiter/pull/4453) Tune batched_gemm_a8w8 per-token-group for large M (MLA absorb bmm)
- [#4834](https://github.com/ROCm/aiter/pull/4834) Add tuned GEMM configs for Kimi-K3 BF16 MoE front shapes
- [#4899](https://github.com/ROCm/aiter/pull/4899) workload-aware KV-split count for auto mode
- [#4835](https://github.com/ROCm/aiter/pull/4835) feat(minimax-m3): add TP8 tuned AITER configs
- [#4918](https://github.com/ROCm/aiter/pull/4918) Retune unified attention configs for gfx950
- [#5028](https://github.com/ROCm/aiter/pull/5028) Tune MoE GEMM A8W8 blockscale
- [#4950](https://github.com/ROCm/aiter/pull/4950) gated_delta_rule: drop removed tl.make_block_ptr; set MHA bwd num_warps=8
- [#5045](https://github.com/ROCm/aiter/pull/5045) Retune GLM5.2 mxfp4 MoE and fix a scale-view cache leak
- [#5004](https://github.com/ROCm/aiter/pull/5004) Optimize sliding-window unified-attention decode
- [#5035](https://github.com/ROCm/aiter/pull/5035) Clamp unified_attention 3D config to the LDS budget on gfx1201
- [#5027](https://github.com/ROCm/aiter/pull/5027) Add head_dim 512 + weightless V-norm to fused_qk_norm_rope_cache_pts_quant_shuffle
- [#5033](https://github.com/ROCm/aiter/pull/5033) Tune MoE GEMM A8W8
- [#4948](https://github.com/ROCm/aiter/pull/4948) Remove legacy flat-layout fallback from GEMM config resolution
- [#4947](https://github.com/ROCm/aiter/pull/4947) unify gluon a8w8 blockscale config resolution
- plus 26 more PRs migrating various GEMM, MoE, and attention configs to the new nested layout ([#5019](https://github.com/ROCm/aiter/pull/5019), [#4933](https://github.com/ROCm/aiter/pull/4933), [#5022](https://github.com/ROCm/aiter/pull/5022), [#5020](https://github.com/ROCm/aiter/pull/5020), [#5018](https://github.com/ROCm/aiter/pull/5018), [#4932](https://github.com/ROCm/aiter/pull/4932), [#4934](https://github.com/ROCm/aiter/pull/4934), [#4927](https://github.com/ROCm/aiter/pull/4927), [#4939](https://github.com/ROCm/aiter/pull/4939), [#4935](https://github.com/ROCm/aiter/pull/4935), [#4936](https://github.com/ROCm/aiter/pull/4936), [#4931](https://github.com/ROCm/aiter/pull/4931), [#4928](https://github.com/ROCm/aiter/pull/4928), [#4929](https://github.com/ROCm/aiter/pull/4929), [#4930](https://github.com/ROCm/aiter/pull/4930), [#4937](https://github.com/ROCm/aiter/pull/4937), [#4938](https://github.com/ROCm/aiter/pull/4938), [#4940](https://github.com/ROCm/aiter/pull/4940), [#4941](https://github.com/ROCm/aiter/pull/4941), [#4942](https://github.com/ROCm/aiter/pull/4942), [#4945](https://github.com/ROCm/aiter/pull/4945), [#4946](https://github.com/ROCm/aiter/pull/4946), [#4944](https://github.com/ROCm/aiter/pull/4944), [#4943](https://github.com/ROCm/aiter/pull/4943), [#4982](https://github.com/ROCm/aiter/pull/4982), [#5021](https://github.com/ROCm/aiter/pull/5021))

</details>

<details>
<summary>Bugfixes (13)</summary>

- [#5054](https://github.com/ROCm/aiter/pull/5054) pin the sweeps that fault, put mori_ep back, fix three…
- [#4952](https://github.com/ROCm/aiter/pull/4952) stabilize GDN prepare triangular solve
- [#4988](https://github.com/ROCm/aiter/pull/4988) Fix compute-bound GEMM A scale TDM inner oob
- [#5006](https://github.com/ROCm/aiter/pull/5006) fix glm5 regression
- [#5034](https://github.com/ROCm/aiter/pull/5034) Fix DSV4 FP4 KV-cache scattered row writes
- [#4994](https://github.com/ROCm/aiter/pull/4994) fuse stage-1 fp8 quant on the heuristic FlyDSL fallback
- [#4964](https://github.com/ROCm/aiter/pull/4964) FIX MLA the nhead fold error for cp round robin
- [#4999](https://github.com/ROCm/aiter/pull/4999) Fix AMDGCN codegen abort in fp8_mqa_logits past ~32K context
- [#4993](https://github.com/ROCm/aiter/pull/4993) Fix PR#4562 and PR#4470 for GPT-OSS-120b on gfx1250
- [#4974](https://github.com/ROCm/aiter/pull/4974) correct output RankData slot prediction during graph capture
- [#4998](https://github.com/ROCm/aiter/pull/4998) Fix caching of dynamic FlyDSL stage2 tensors
- [#5042](https://github.com/ROCm/aiter/pull/5042) correct lambda arity in ob::radix_kernel / last_filter_kernel
- [#4957](https://github.com/ROCm/aiter/pull/4957) Fix gfx942 gqa64 sparse-MLA decode GPU fault (route to capture-safe fold)

</details>

<details>
<summary>CI & build (15)</summary>

- [#4887](https://github.com/ROCm/aiter/pull/4887) remove lean_atten files and relevant imports in aiter
- [#5014](https://github.com/ROCm/aiter/pull/5014) Add hardware and DeepSeek-V4 performance suites
- [#4975](https://github.com/ROCm/aiter/pull/4975) Add MK1 persistent decoder provider
- [#4962](https://github.com/ROCm/aiter/pull/4962) add Kimi and MiniMax to ATOM DI matrix
- [#4996](https://github.com/ROCm/aiter/pull/4996) JIT: use torch's bundled pybind11 to avoid ABI (internals-version) skew
- plus 10 more minor CI, test, and build updates ([#5050](https://github.com/ROCm/aiter/pull/5050), [#5008](https://github.com/ROCm/aiter/pull/5008), [#5003](https://github.com/ROCm/aiter/pull/5003), [#4912](https://github.com/ROCm/aiter/pull/4912), [#4969](https://github.com/ROCm/aiter/pull/4969), [#4956](https://github.com/ROCm/aiter/pull/4956), [#4959](https://github.com/ROCm/aiter/pull/4959), [#4972](https://github.com/ROCm/aiter/pull/4972), [#5057](https://github.com/ROCm/aiter/pull/5057), [#4925](https://github.com/ROCm/aiter/pull/4925))

</details>

<details>
<summary>Docs (2)</summary>

- [#4973](https://github.com/ROCm/aiter/pull/4973) Update Gluon GEMM-A8W8_BLOCKSCALE README to match nested config layout and supported archs
- [#4923](https://github.com/ROCm/aiter/pull/4923) fix MI300A gfx target in attention docs (gfx942, not gfx950)

</details>

<details>
<summary>Refactors (2)</summary>

- [#5051](https://github.com/ROCm/aiter/pull/5051) Chore/port flydsl kernel code cleanup skill
- [#4963](https://github.com/ROCm/aiter/pull/4963) gfx942 fp8_mqa_logits: let _auto_variant choose rows_per_block

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 1c04bdaf235125d1747271f5711b5f344b9b5176967d82e92f03b8e1369417dc -->
