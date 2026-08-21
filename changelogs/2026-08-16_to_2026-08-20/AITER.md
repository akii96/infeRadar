# AITER: PR digest (2026-08-16 to 2026-08-20)

_48 merged, 58 newly opened - source ROCm/AITER, generated 2026-08-20T09:33:54Z_

## TL;DR
- DeepSeek, Kimi, and MiniMax dominated this window, with major performance work targeting MoE GEMMs (A8W4, A4W4, MXFP4) and attention kernels on gfx950 and gfx1250 architectures.
- Merged a massive MHA v4 entrypoint supporting a wide spectrum of quantized and sparse attention kernels, alongside ongoing work to bring MLA to gfx1250 via FlyDSL.
- Significant push on low-bitweight MoE, including unifying A8W4 metadata dispatch, optimizing FlyDSL MoE GEMMs, and introducing new MXFP4/MXFP6 kernels for Qwen and DeepSeek.
- The codebase is aggressively shedding technical debt, highlighted by massive in-progress PRs ripping out legacy MoE implementations in both Triton/Gluon and FlyDSL backends.

## Most important PRs
- **[#4627](https://github.com/ROCm/aiter/pull/4627)** Introduces the MHA v4 entrypoint and a broad suite of quantized and sparse attention kernels for gfx942 and gfx950. This establishes a unified, high-performance foundation for next-generation attention variants across ASM, HIP, and Triton backends.
- **[#4864](https://github.com/ROCm/aiter/pull/4864)** (Newly opened) Achieves a massive 31% performance improvement over hipBLASLt for Kimi-K3 BF16 TN GEMM front projections on gfx950 by leveraging a tuned FlyDSL/ASM implementation.
- **[#4833](https://github.com/ROCm/aiter/pull/4833)** (Newly opened) Deletes over 9,000 lines of legacy Triton/Gluon MoE code. This signals a major architectural shift toward the newer, unified MoE dispatch and quantization paths.
- **[#4869](https://github.com/ROCm/aiter/pull/4869)** (Newly opened) Heavily optimizes Conv2D operations for RDNA architectures (gfx1201/gfx1250) and CDNA (gfx942/gfx950), overhauling the kernels, routing logic, and input packing strategies.
- **[#4730](https://github.com/ROCm/aiter/pull/4730)** Delivers substantial FlyDSL MoE GEMM optimizations specifically targeted at gfx1250. This improves execution efficiency for low-bitweight quantized expert routing.

## More changes by area

<details>
<summary>Performance (19)</summary>

- [#4749](https://github.com/ROCm/aiter/pull/4749) Tune BF16 GEMM for DeepSeek on gfx1250
- [#4804](https://github.com/ROCm/aiter/pull/4804) Tune BF16 GEMM for gfx1250 DeepSeek-V4-Flash shapes
- [#4760](https://github.com/ROCm/aiter/pull/4760) Update A8W8 GEMM tuned config for DeepSeek on gfx1250 FlyDSL
- [#4767](https://github.com/ROCm/aiter/pull/4767) Add MXFP4 fused-MoE configs for Qwen on gfx950 (TP8)
- [#4759](https://github.com/ROCm/aiter/pull/4759) Add full 16-tier Qwen3-VL FP4 MoE tuned config for gfx950
- [#4801](https://github.com/ROCm/aiter/pull/4801) Improve A4W4 tuning config for gfx1250 FlyDSL
- [#4781](https://github.com/ROCm/aiter/pull/4781) Retune small-M tiles and wave counts in A16W16 fallback config for gfx950
- [#4718](https://github.com/ROCm/aiter/pull/4718) Tune chunked_pa_prefill params for gfx950 Triton/Gluon
- [#4733](https://github.com/ROCm/aiter/pull/4733) Improve HD256 FP8 attention performance on gfx950
- [#4849](https://github.com/ROCm/aiter/pull/4849) [Opened] Optimize A8W8 MX128 bpreshuffle GEMM for DeepSeek on gfx1250
- [#4816](https://github.com/ROCm/aiter/pull/4816) [Opened] Add DeepSeek-V4 A8W8 blockscale GEMM configs for gfx942
- [#4851](https://github.com/ROCm/aiter/pull/4851) [Opened] Add gfx1250 A16W16 GEMM configs for FLUX.2 shapes
- [#4815](https://github.com/ROCm/aiter/pull/4815) [Opened] Add Qwen3.6 35B-A3B FMoE configs for gfx1201
- [#4873](https://github.com/ROCm/aiter/pull/4873) [Opened] Tune Kimi-K3 A4W4 and FP8 projections for gfx950
- [#4824](https://github.com/ROCm/aiter/pull/4824) [Opened] Add DeepSeek-V4 MoE config on gfx1250
- [#4814](https://github.com/ROCm/aiter/pull/4814) [Opened] Enable GEMM-A16W16 tuning on gfx1151
- [#4835](https://github.com/ROCm/aiter/pull/4835) [Opened] Add TP8 tuned AITER configs for MiniMax-M3
- [#4834](https://github.com/ROCm/aiter/pull/4834) [Opened] Add tuned GEMM configs for Kimi-K3 BF16 MoE front shapes
- [#4798](https://github.com/ROCm/aiter/pull/4798) Retune GLM-5 MXFP4 MoE token=8 to A4W4

</details>

<details>
<summary>Kernels & attention (14)</summary>

- [#4796](https://github.com/ROCm/aiter/pull/4796) Detorch reduce.cu and delete dead Python port for MLA
- [#4792](https://github.com/ROCm/aiter/pull/4792) Revert relocation of MLA Gluon kernel and unified decode dispatch on gfx950
- [#4736](https://github.com/ROCm/aiter/pull/4736) Replace block_ptr in HSTU attention kernel
- [#4862](https://github.com/ROCm/aiter/pull/4862) [Opened] Add MLA support for gfx1250 via FlyDSL
- [#4787](https://github.com/ROCm/aiter/pull/4787) [Opened] Optimize MiniMax M3 scoring and top-k kernels on gfx950
- [#4875](https://github.com/ROCm/aiter/pull/4875) [Opened] Add gfx942 FMHA varlen backward kernel for d_qk=192/d_v=128
- [#4803](https://github.com/ROCm/aiter/pull/4803) [Opened] Implement fused_clamp_act_mul Gluon kernel
- [#4860](https://github.com/ROCm/aiter/pull/4860) [Opened] Add BF16 persistent GEMM for gfx1250 Gluon
- [#4794](https://github.com/ROCm/aiter/pull/4794) [Opened] Add Chefang/PA decode for Opus via HIP
- [#4863](https://github.com/ROCm/aiter/pull/4863) [Opened] Add Kimi-K3 AttnResidual score and combine ASM kernel
- [#4877](https://github.com/ROCm/aiter/pull/4877) [Opened] Support LSE in OPUS MHA on gfx950
- [#4810](https://github.com/ROCm/aiter/pull/4810) [Opened] Register FlyDSL MLA and attention ops in PyTorch
- [#4852](https://github.com/ROCm/aiter/pull/4852) [Opened] Replace BF16 prefill MHA kernel for gfx1250 ASM
- [#4756](https://github.com/ROCm/aiter/pull/4756) Remove vestigial py_itfs_common.h includes and make top_k_per_row torch-free

</details>

<details>
<summary>MoE & quantization (18)</summary>

- [#4460](https://github.com/ROCm/aiter/pull/4460) Support softmax + need_renorm in topk_gating and refactor tests
- [#4755](https://github.com/ROCm/aiter/pull/4755) Unify A8W4 metadata and runtime dispatch for Opus MoE
- [#4446](https://github.com/ROCm/aiter/pull/4446) Add moe_a16w4 gfx1250 Gluon kernel
- [#4655](https://github.com/ROCm/aiter/pull/4655) Add support for v2 gemm2 A8W8 for MiniMax via FlyDSL
- [#4826](https://github.com/ROCm/aiter/pull/4826) Use new preshuffling API for A4W4 MoE on gfx1250 Gluon
- [#4876](https://github.com/ROCm/aiter/pull/4876) [Opened] Remove legacy flydsl_moe2 v1 code
- [#4785](https://github.com/ROCm/aiter/pull/4785) [Opened] Implement mega-moe stage2 for gfx1250 FlyDSL
- [#4859](https://github.com/ROCm/aiter/pull/4859) [Opened] Clean up MXFP6 GEMMs for gfx950 ASM/HIP
- [#4789](https://github.com/ROCm/aiter/pull/4789) [Opened] Update GEMM stage2 v2 kernel for FlyDSL
- [#4837](https://github.com/ROCm/aiter/pull/4837) [Opened] Add GEMM amxfp8wmxfp8 kernel for gfx950 Triton
- [#4850](https://github.com/ROCm/aiter/pull/4850) [Opened] Add gradlib GEMM, moe_mxfp4_aux, and custom all-reduce for gfx1250
- [#4782](https://github.com/ROCm/aiter/pull/4782) [Opened] Add direct dense A4W4 MXFP4 GEMM for gfx950 FlyDSL
- [#4848](https://github.com/ROCm/aiter/pull/4848) [Opened] Address expert weights past 4 GB in MoE GEMMs
- [#4866](https://github.com/ROCm/aiter/pull/4866) [Opened] Move Gluon gemm_a8w8 kernel into gfx950 specific directory
- [#4836](https://github.com/ROCm/aiter/pull/4836) [Opened] Add Triton support for gfx1250 MoE A8W4 and A4W4
- [#4879](https://github.com/ROCm/aiter/pull/4879) [Opened] Optimize MXFP4 MoE stage2 v2 for FlyDSL
- [#4878](https://github.com/ROCm/aiter/pull/4878) [Opened] Disable Gluon for Triton FP4 GEMM on gfx1250
- [#4845](https://github.com/ROCm/aiter/pull/4845) [Opened] Support mixed-dtype inputs in biased grouped top-k

</details>

<details>
<summary>Parallelism & scheduling (5)</summary>

- [#4832](https://github.com/ROCm/aiter/pull/4832) Detorch fused_ar_mhc_post and add pybind
- [#4753](https://github.com/ROCm/aiter/pull/4753) Fix LL proto all-reduce dispatch
- [#4821](https://github.com/ROCm/aiter/pull/4821) [Opened] Implement TDM dispatch transport for gfx1250
- [#4812](https://github.com/ROCm/aiter/pull/4812) [Opened] Fix gfx1250 custom all-reduce input publication in NPS2/DPX mode
- [#4786](https://github.com/ROCm/aiter/pull/4786) [Opened] Use SYSTEM scope and ACQUIRE ordering for cross-device signal loads

</details>

<details>
<summary>Model support (4)</summary>

- [#4707](https://github.com/ROCm/aiter/pull/4707) Stabilize SiTUv2 AOT cache keys in FlyDSL
- [#4697](https://github.com/ROCm/aiter/pull/4697) Cover int32 slot_mapping in KV cache tests
- [#4813](https://github.com/ROCm/aiter/pull/4813) [Opened] Implement fused MiniMax-M3 QKNorm + RoPE + CacheInsert
- [#4800](https://github.com/ROCm/aiter/pull/4800) [Opened] Make blob codegen cache publication transactional

</details>

<details>
<summary>Bugfixes (19)</summary>

- [#4847](https://github.com/ROCm/aiter/pull/4847) Fix OPUS MHA TypeError issue on gfx950 HIP
- [#4843](https://github.com/ROCm/aiter/pull/4843) Support ROCm 10 by dropping hipcub::Traits dependency in sampling
- [#4829](https://github.com/ROCm/aiter/pull/4829) Lazily dequantize MoE reference weights
- [#4853](https://github.com/ROCm/aiter/pull/4853) Support ROCm 10 by dropping hipcub::Traits dependency in topk_per_row
- [#4774](https://github.com/ROCm/aiter/pull/4774) Fix 32-bit KV block offsets in Gluon paged-MQA logits kernel
- [#4742](https://github.com/ROCm/aiter/pull/4742) Tolerate missing original_max_position_embeddings in RoPE
- [#4858](https://github.com/ROCm/aiter/pull/4858) Fix DeepSeek-V3 shape regression in FlyDSL
- [#4811](https://github.com/ROCm/aiter/pull/4811) Retune GLM-5 FP8 decode kernels to fix FMoE issues
- [#4844](https://github.com/ROCm/aiter/pull/4844) Fix MoE unit test OOM
- [#4806](https://github.com/ROCm/aiter/pull/4806) [Opened] Fix and optimize inverse RoPE group quantization on gfx1250
- [#4809](https://github.com/ROCm/aiter/pull/4809) [Opened] Fix lean attention for gfx950
- [#4868](https://github.com/ROCm/aiter/pull/4868) [Opened] Guard RDNA unified attention against LDS overflow
- [#4817](https://github.com/ROCm/aiter/pull/4817) [Opened] Support torch.Stream in ctypes conversion
- [#4825](https://github.com/ROCm/aiter/pull/4825) [Opened] Fix non-stage1 paged MQA logits for KV block size > 1 for DeepSeek
- [#4797](https://github.com/ROCm/aiter/pull/4797) [Opened] Generate CK FMHA kernels for gfx1250
- [#4839](https://github.com/ROCm/aiter/pull/4839) [Opened] Guard against negative expert IDs in MoE sorting P0
- [#4841](https://github.com/ROCm/aiter/pull/4841) [Opened] Add acquire fence for MB radix barrier last block
- [#4880](https://github.com/ROCm/aiter/pull/4880) [Opened] Fix pa_prefill performance regression for small HEAD_DIM
- [#4872](https://github.com/ROCm/aiter/pull/4872) [Opened] Fold FP8 qlen 2 onto the qseqlen-4 kernel on gfx950

</details>

<details>
<summary>CI & build (21)</summary>

- [#4651](https://github.com/ROCm/aiter/pull/4651) Use shared runtime GPU architecture detection
- [#4436](https://github.com/ROCm/aiter/pull/4436) Update FlyDSL version and adapt kernels to internal LLVM ROCDL API changes
- [#4870](https://github.com/ROCm/aiter/pull/4870) [Opened] Add validate-kernel-pr skill and structural D9 trigger for review-pr
- plus 18 more minor CI, build, and test updates

</details>

<details>
<summary>Other (1)</summary>

- [#4793](https://github.com/ROCm/aiter/pull/4793) Resolve pybind develop-path lookups once instead of per call

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: fb35f514f455a4ed131859448c539bae5995adca69687d360d07c620bdcbdaf3 -->
