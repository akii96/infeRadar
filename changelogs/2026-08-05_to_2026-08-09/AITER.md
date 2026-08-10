# AITER: PR digest (2026-08-05 to 2026-08-09)

_45 merged, 50 newly opened - source ROCm/AITER, generated 2026-08-09T21:35:29Z_

## TL;DR
- **Model Focus**: Kimi and DeepSeek drove the majority of development this cycle, with significant performance tuning also landing for GLM and Qwen.
- **Attention & MLA**: Major architectural upgrades hit the attention pipelines, including a massive new MHA v4 entrypoint and extensive MLA support (MI350 PS mode, CDNA3 decode, and unified Gluon kernels).
- **MoE & Quantization**: Heavy churn occurred in MoE kernels, notably replacing the old a16w4 kernel with a faster SiTUv2 implementation for Kimi, alongside broad MXFP4 and FP8 tuning.
- **Framework Evolution**: The FlyDSL and Gluon backends saw substantial refactoring (tiled-copy, TDM) and new kernel additions to support chunked delta attention and unified attention.

## Most important PRs
- **[#4502](https://github.com/ROCm/aiter/pull/4502)** Replaces the legacy a16w4 MoE kernel with a significantly faster SiTUv2 implementation (bf16 A x MXFP4 W), delivering major performance wins for Kimi.
- **[#4627](https://github.com/ROCm/aiter/pull/4627)** Introduces a massive new MHA v4 entrypoint, unifying a wide spectrum of quantized and sparse attention kernels under a single architecture.
- **[#4602](https://github.com/ROCm/aiter/pull/4602)** Adds highly optimized Triton kernels for chunk delta attention, significantly improving Kimi's attention performance on gfx950.
- **[#4646](https://github.com/ROCm/aiter/pull/4646)** Ports the a16wi4 MoE implementation to a new FlyDSL pipeline, cleaning up the legacy 2-stage MoE GEMM code.
- **[#4430](https://github.com/ROCm/aiter/pull/4430)** Implements a new DeepSeek opus kernel for MLA PS mode on MI350, specifically targeting the `nhead*qseqlen=128` case for better throughput.

## More changes by area

<details>
<summary>Kernels & attention (21)</summary>

- [#3901](https://github.com/ROCm/aiter/pull/3901) Adds a FlyDSL MLA reduce decode kernel for gfx942
- [#4382](https://github.com/ROCm/aiter/pull/4382) Implements a paged sparse attention Gluon kernel for DeepSeek on gfx950
- [#4576](https://github.com/ROCm/aiter/pull/4576) Merges the Gluon DSv4 attention prefill API entry with `pa_prefill_sparse`
- [#3936](https://github.com/ROCm/aiter/pull/3936) Introduces XCD-aware spatial workgroup mapping for MHA and GQA
- [#4573](https://github.com/ROCm/aiter/pull/4573) Supports strided GDN decode state routing in FlyDSL
- [#4575](https://github.com/ROCm/aiter/pull/4575) Replaces KV buffer loads with 64-bit global loads in DSv4 prefill
- [#4521](https://github.com/ROCm/aiter/pull/4521) Adds round-robin compute partition support for MLA PS mode FP8
- [#4591](https://github.com/ROCm/aiter/pull/4591) Disables `amdgpu-early-inline-all` for DSv4 sparse prefill
- [#4568](https://github.com/ROCm/aiter/pull/4568) Adds Triton kernels for chunk delta attention targeting Kimi
- [#4645](https://github.com/ROCm/aiter/pull/4645) Implements FP8 D192/V128 prefill for Kimi on gfx942 Gluon
- [#4584](https://github.com/ROCm/aiter/pull/4584) Adds KDA Gluon implementation for gfx1250
- [#4614](https://github.com/ROCm/aiter/pull/4614) Introduces a unified attention Gluon kernel for gfx950
- [#4598](https://github.com/ROCm/aiter/pull/4598) Adds a fused intra-chunk GDN prefill prepare kernel in FlyDSL
- [#4616](https://github.com/ROCm/aiter/pull/4616) Implements a BF16 MLA kernel in FlyDSL for gfx1250
- [#4577](https://github.com/ROCm/aiter/pull/4577) Enables KDA per-channel decay gate in FlyDSL GDR decode for Kimi
- [#4582](https://github.com/ROCm/aiter/pull/4582) Adds a CDNA3 decode kernel for MLA on gfx942
- [#4626](https://github.com/ROCm/aiter/pull/4626) Implements batched GEMM in FlyDSL for gfx1250
- [#4572](https://github.com/ROCm/aiter/pull/4572) Adds an attention residual Triton kernel for Kimi-K3
- [#4610](https://github.com/ROCm/aiter/pull/4610) Implements attention residual in FlyDSL
- [#4565](https://github.com/ROCm/aiter/pull/4565) Supports mask0 for MI350 MLA PS mode BF16
- [#4625](https://github.com/ROCm/aiter/pull/4625) Supports 96-head 128-dim reduction for MLA

</details>

<details>
<summary>MoE & quantization (14)</summary>

- [#4596](https://github.com/ROCm/aiter/pull/4596) Extracts MoE reduce operations into a dedicated kernel
- [#4534](https://github.com/ROCm/aiter/pull/4534) Optimizes opus MoE SiTUv2 capabilities for Kimi on gfx950
- [#4564](https://github.com/ROCm/aiter/pull/4564) Implements asynchronous scales for a8w4 MoE
- [#4362](https://github.com/ROCm/aiter/pull/4362) Adds unit-scale FP8 KV cache support to `fused_qknorm_idxrqknorm`
- [#4445](https://github.com/ROCm/aiter/pull/4445) Re-enables FP4 KV cache for UA and MLA on gfx1250
- [#4595](https://github.com/ROCm/aiter/pull/4595) Optimizes FMoE GEMM v2 tile size to 128x256x256
- [#4640](https://github.com/ROCm/aiter/pull/4640) Enables MXFP4 MoE support for gfx1100 in Triton
- [#4597](https://github.com/ROCm/aiter/pull/4597) Improves tiny kernel performance for MoE on gfx1250
- [#4586](https://github.com/ROCm/aiter/pull/4586) Supports sorted intermediate layouts for opus MoE
- [#4607](https://github.com/ROCm/aiter/pull/4607) Fuses A4W4 stage-1 FP4 quantization on gfx1250
- [#4641](https://github.com/ROCm/aiter/pull/4641) Adds SwiGLU activation to the 2-stage MoE GEMM stage-1 kernel
- [#4647](https://github.com/ROCm/aiter/pull/4647) Reuses stage-1 scratch buffers across layers and graph captures
- [#4620](https://github.com/ROCm/aiter/pull/4620) Adds GeLU with tanh approximation for CK XDL 2-stage MoE
- [#4617](https://github.com/ROCm/aiter/pull/4617) Updates fused MoE to accept caller-provided output buffers

</details>

<details>
<summary>Performance & tuning (17)</summary>

- [#4265](https://github.com/ROCm/aiter/pull/4265) Enables conv2d Triton kernels for RDNA3 and RDNA3.5
- [#4563](https://github.com/ROCm/aiter/pull/4563) Tunes prefill MQA logits kernels for GLM-5.x
- [#4396](https://github.com/ROCm/aiter/pull/4396) Tunes a8w8 GEMM for Qwen3.5 MXFP4-AttnFP8
- [#4223](https://github.com/ROCm/aiter/pull/4223) Tunes fuse-aware gfx950 fused GEMM A8W8 blockscale
- [#4558](https://github.com/ROCm/aiter/pull/4558) Dispatches a16 FMoE kernels for GLM-5 decode on gfx942
- [#3739](https://github.com/ROCm/aiter/pull/3739) Adds DSv3-MXFP4 fused-MoE shape configurations
- [#4414](https://github.com/ROCm/aiter/pull/4414) Tunes MHA config to address small-head pipeline pathology
- [#4552](https://github.com/ROCm/aiter/pull/4552) Routes missing Kimi-K3 fused BF16 GEMM to Triton on gfx1250
- [#4570](https://github.com/ROCm/aiter/pull/4570) Adds tuned BF16 GEMM config for Qwen3-8B on gfx950
- [#4513](https://github.com/ROCm/aiter/pull/4513) Tunes MXMoE kernels for Qwen3.5-397B TP2 decode
- [#4571](https://github.com/ROCm/aiter/pull/4571) Optimizes group MoE small operations on gfx1250
- [#4642](https://github.com/ROCm/aiter/pull/4642) Optimizes MoE MXFP4 stage-2 for Kimi on gfx950
- [#4613](https://github.com/ROCm/aiter/pull/4613) Adds dtype directories to tuning configurations
- [#4603](https://github.com/ROCm/aiter/pull/4603) Tunes Kimi-K3 A4W4 configs on gfx950
- [#4592](https://github.com/ROCm/aiter/pull/4592) Adds BF16 GEMM config for DSv4 on gfx1250
- [#4629](https://github.com/ROCm/aiter/pull/4629) Retunes MXFP4 fused-MoE for GLM-5.2 on gfx950
- [#4632](https://github.com/ROCm/aiter/pull/4632) Tunes MLA decode RoPE FP32 config for gfx950

</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- [#4605](https://github.com/ROCm/aiter/pull/4605) Fixes the `reduce_scatter` PyNCCL path
- [#4478](https://github.com/ROCm/aiter/pull/4478) Forwards `transpose_scale` through fused AllReduce + RMSNorm
- [#4547](https://github.com/ROCm/aiter/pull/4547) Cherry-picks a fix for custom all-reduce in Qwen3.5

</details>

<details>
<summary>Refactors (9)</summary>

- [#4606](https://github.com/ROCm/aiter/pull/4606) Refactors FlyDSL tiled-copy for SwiGLU, SiLU, and FP8 MQA
- [#4609](https://github.com/ROCm/aiter/pull/4609) Cleans up FlyDSL raw-dialect for GDR decode and chunked delta attention
- [#4569](https://github.com/ROCm/aiter/pull/4569) Refactors and detorches `module_sample`
- [#4590](https://github.com/ROCm/aiter/pull/4590) Refactors and detorches `module_aiter_unary`
- [#4599](https://github.com/ROCm/aiter/pull/4599) Refactors TDM implementation for gfx1250
- [#4622](https://github.com/ROCm/aiter/pull/4622) Replaces split-K atomic combine with a workspace and reduce kernel
- [#4630](https://github.com/ROCm/aiter/pull/4630) Unifies configuration loading and adds unit tests
- [#4594](https://github.com/ROCm/aiter/pull/4594) Cleans up rocPRIM and hipCUB usage in HIP kernels
- [#4615](https://github.com/ROCm/aiter/pull/4615) Registers FlyDSL operations directly in PyTorch

</details>

<details>
<summary>Bugfixes (17)</summary>

- [#4452](https://github.com/ROCm/aiter/pull/4452) Refreshes gfx950 MLA HSACO for large `page_id` KV addressing
- [#4543](https://github.com/ROCm/aiter/pull/4543) Fixes MXMoE GEMM2 implementation
- [#4579](https://github.com/ROCm/aiter/pull/4579) Removes block pointers in `lean_atten_paged.py` to fix large-KV indexing
- [#4588](https://github.com/ROCm/aiter/pull/4588) Fixes `shuffle_scale_moe` crashing with `UnboundLocalError` on gfx942
- [#4567](https://github.com/ROCm/aiter/pull/4567) Adds an assertion for LayerNorm weight/input dtype mismatches
- [#4546](https://github.com/ROCm/aiter/pull/4546) Fixes out-of-bounds scale descriptor in PTPC FP8 GEMM
- [#4635](https://github.com/ROCm/aiter/pull/4635) Fixes vector imports for FlyDSL
- [#4581](https://github.com/ROCm/aiter/pull/4581) Makes blockscale split-K deterministic
- [#4587](https://github.com/ROCm/aiter/pull/4587) Keeps `get_meta_param` split-offset tables alive for captured CUDA graphs
- [#4566](https://github.com/ROCm/aiter/pull/4566) Isolates AITER extensions from HIP interposers
- [#4580](https://github.com/ROCm/aiter/pull/4580) Guards all `OutLogits` stores in `pa_mqa_logits`
- [#4612](https://github.com/ROCm/aiter/pull/4612) Fixes MHA behavior with softmax-sink
- [#4621](https://github.com/ROCm/aiter/pull/4621) Fixes graph mode errors when PyTorch sets `expandable_segments:True`
- [#4637](https://github.com/ROCm/aiter/pull/4637) Rounds scaled INT8 casts to nearest
- [#4639](https://github.com/ROCm/aiter/pull/4639) Fixes hipify qualifier loss and `std::min` build failures
- [#4628](https://github.com/ROCm/aiter/pull/4628) Restores gfx942 FLAT kernel support for fused MoE
- [#4578](https://github.com/ROCm/aiter/pull/4578) Swaps gfx950 kernel to hold 64-bit memory addresses

</details>

<details>
<summary>CI & build (9)</summary>

- [#4608](https://github.com/ROCm/aiter/pull/4608) Fixes ROCK compilation issues
- [#4623](https://github.com/ROCm/aiter/pull/4623) Fixes profiler `UnicodeDecodeError` in AITER tests
- [#4593](https://github.com/ROCm/aiter/pull/4593) Drops redundant `aiter::` prefix from define schema for PyTorch 2.13
- [#4589](https://github.com/ROCm/aiter/pull/4589) Temporarily pins the `rocm/pytorch:latest` image digest
- [#4413](https://github.com/ROCm/aiter/pull/4413) Defaults `mp_tuner` timeout to reap dead workers instead of hanging
- [#4600](https://github.com/ROCm/aiter/pull/4600) Moves multi-GPU tests to the DO MI350X runner
- [#4619](https://github.com/ROCm/aiter/pull/4619) Runs vLLM disagg from upstream main
- [#4624](https://github.com/ROCm/aiter/pull/4624) Resolves container Python versions for release builds
- [#4611](https://github.com/ROCm/aiter/pull/4611) Drops per-kernel compile logs and silences false-positive MXMoE warnings

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: c2fcf6a17187c6a013166232517753b20837f35c84bf399ca858126d71607f50 -->
