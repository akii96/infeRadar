# AITER: PR digest (2026-08-19 to 2026-08-23)

_49 merged, 68 newly opened - source ROCm/AITER, generated 2026-08-23T21:24:39Z_

## TL;DR
*   **DeepSeek and Kimi dominated** this cycle, with major performance pushes for MoE, Multi-Head Latent Attention (MLA), and low-bit quantization (mxfp4/mxfp8, a8w4, a4w4) on AMD hardware (gfx1250, gfx950).
*   **MoE & Quantization wins:** Significant merged work on FlyDSL and Triton/Gluon backends for MoE GEMMs, including mega-MoE stage 2 for gfx1250, mxfp8 GEMM, and unified A8W4 dispatch.
*   **Attention & Kernel advances:** Newly opened work introduces Sparse Paged Attention, Sparse MLA for gfx950, and fused K5/K6 linear attention prefill kernels.
*   **Massive config refactor:** An in-progress architectural shift is migrating all Triton/Gluon GEMM configurations (A16W16, A8W8, MXFP4, blockscale) to a new nested layout to streamline tuning resolution.

## Most important PRs
*   **[#4903](https://github.com/ROCm/aiter/pull/4903)** Integrates the OPUS BF16 GEMM co-processor path for DeepSeek on gfx1250. This massive 22k-line newly opened architectural addition significantly bolsters BF16 throughput for DeepSeek models.
*   **[#4785](https://github.com/ROCm/aiter/pull/4785)** Implements "mega-MoE" stage 2 support for gfx1250 via FlyDSL. This merged feature significantly advances distributed MoE routing and communication capabilities for large-scale models.
*   **[#4732](https://github.com/ROCm/aiter/pull/4732)** Adds prefill GDN K5 fp32 chunk states and AOT coverage across Triton, Gluon, and FlyDSL. This directly improves Qwen attention prefill performance and state management.
*   **[#4773](https://github.com/ROCm/aiter/pull/4773)** Delivers Triton/Gluon mxfp8 GEMM kernels for gfx1250, gfx950, and gfx942. This unlocks critical low-bit quantization performance and memory bandwidth savings for DeepSeek.
*   **[#4919](https://github.com/ROCm/aiter/pull/4919)** Introduces Sparse Paged Attention and Sparse Multi-Head Latent Attention (MLA) for gfx950. This newly opened work optimizes memory and throughput for long-context workloads.

## More changes by area

<details>
<summary>MoE & quantization (27)</summary>

- [#4755](https://github.com/ROCm/aiter/pull/4755) Unifies A8W4 metadata and runtime dispatch for Opus MoE
- [#4849](https://github.com/ROCm/aiter/pull/4849) Optimizes a8w8 mx128 block preshuffle GEMM for gfx1250
- [#4806](https://github.com/ROCm/aiter/pull/4806) Fixes and optimizes inverse RoPE group quantization on gfx1250
- [#4730](https://github.com/ROCm/aiter/pull/4730) Optimizes FlyDSL MoE GEMM performance
- [#4891](https://github.com/ROCm/aiter/pull/4891) Adds native-I384 DeepSeek V4 support through M=2048 for FlyDSL FHMoE
- [#4892](https://github.com/ROCm/aiter/pull/4892) Tunes MoE A8W4 configurations for Triton/Gluon
- [#4879](https://github.com/ROCm/aiter/pull/4879) Optimizes mxfp4 MoE stage 2 (v2)
- [#4904](https://github.com/ROCm/aiter/pull/4904) Improves tiny kernel performance for MoE quantization
- [#4836](https://github.com/ROCm/aiter/pull/4836) Adds Triton support for gfx1250 MoE a8w4 and a4w4
- [#4597](https://github.com/ROCm/aiter/pull/4597) Improves tiny kernel for FlyDSL MoE
- [#4898](https://github.com/ROCm/aiter/pull/4898) Reverts tiny kernel improvements for FlyDSL MoE
- [#4826](https://github.com/ROCm/aiter/pull/4826) Updates a4w4 MoE to use the new preshuffling API on gfx1250
- [#4914](https://github.com/ROCm/aiter/pull/4914) Tunes a4w4 CSV configurations
- [#4829](https://github.com/ROCm/aiter/pull/4829) Fixes lazy dequantization of MoE reference weights in CI
- [#4873](https://github.com/ROCm/aiter/pull/4873) Tunes Kimi-K3 A4W4 and FP8 projections for gfx950
- [#4901](https://github.com/ROCm/aiter/pull/4901) Skips memory-heavy MoE 2-stage test cases
- [#4835](https://github.com/ROCm/aiter/pull/4835) Adds TP8 tuned AITER configs for MiniMax-m3
- [#4911](https://github.com/ROCm/aiter/pull/4911) Fixes a4w4 MoE prefill kernel in FlyDSL
- [#4900](https://github.com/ROCm/aiter/pull/4900) Moves mxfp4 preshuffled configs into correct folders
- [#4858](https://github.com/ROCm/aiter/pull/4858) Fixes DeepSeek V3 shape regression in FlyDSL
- [#4876](https://github.com/ROCm/aiter/pull/4876) Removes legacy FlyDSL MoE v1 code
- [#4894](https://github.com/ROCm/aiter/pull/4894) Adds MXFP4/MXFP8 Gluon quantization kernels for gfx950/gfx1250
- [#4848](https://github.com/ROCm/aiter/pull/4848) Addresses expert weights exceeding 4GB in MoE GEMMs
- [#4906](https://github.com/ROCm/aiter/pull/4906) Updates gfx950 layout for fmoe2 CSV
- [#4845](https://github.com/ROCm/aiter/pull/4845) Supports mixed-dtype inputs in biased grouped top-k
- [#4890](https://github.com/ROCm/aiter/pull/4890) Adds 1x32 mxfp4 ASM kernel for gfx950
- [#4854](https://github.com/ROCm/aiter/pull/4854) Re-enables MoE 2-stage tests in CI
</details>

<details>
<summary>Kernels & attention (31)</summary>

- [#4850](https://github.com/ROCm/aiter/pull/4850) Integrates gradlib GEMM, moe_mxfp4_aux, mha_native_splitkv, and custom all-reduce for gfx1250
- [#4626](https://github.com/ROCm/aiter/pull/4626) Implements FlyDSL batched GEMM for gfx1250
- [#4776](https://github.com/ROCm/aiter/pull/4776) Chunks the non-FP4 gather_kv_b_proj over KV for MLA performance
- [#4531](https://github.com/ROCm/aiter/pull/4531) Updates mRoPE cache-quant to accept strided flash KV-cache views
- [#4847](https://github.com/ROCm/aiter/pull/4847) Fixes OPUS MHA TypeError issue on gfx950
- [#4852](https://github.com/ROCm/aiter/pull/4852) Replaces bf16 prefill MHA kernel with ASM implementation on gfx1250
- [#4907](https://github.com/ROCm/aiter/pull/4907) Adds GDN MTP kernels for causal conv1d update and gated delta rule
- [#4884](https://github.com/ROCm/aiter/pull/4884) Fuses K5 + K6 gfx942 kernel for linear attention prefill
- [#4885](https://github.com/ROCm/aiter/pull/4885) Adds HSTU Backward kernel to FlyDSL
- [#4887](https://github.com/ROCm/aiter/pull/4887) Removes lean_atten files and relevant imports
- [#4869](https://github.com/ROCm/aiter/pull/4869) Optimizes conv2d for RDNA (kernels, routing, and input packing)
- [#4862](https://github.com/ROCm/aiter/pull/4862) Adds MLA support for gfx1250 in FlyDSL
- [#4859](https://github.com/ROCm/aiter/pull/4859) Implements Mxfp6 GEMMs via ASM/HIP JIT
- [#4882](https://github.com/ROCm/aiter/pull/4882) Adds paged sparse attention kernels for Triton/Gluon
- [#4864](https://github.com/ROCm/aiter/pull/4864) Tunes BF16 TN GEMM for Kimi-K3 front projection on gfx950 via ASM
- [#4875](https://github.com/ROCm/aiter/pull/4875) Adds gfx942 FMHA varlen backward kernel for d_qk=192/d_v=128
- [#4860](https://github.com/ROCm/aiter/pull/4860) Implements BF16 persistent GEMM for Triton/Gluon
- [#4863](https://github.com/ROCm/aiter/pull/4863) Adds Kimi-K3 AttnResidual score and combines ASM kernel
- [#4926](https://github.com/ROCm/aiter/pull/4926) Adds MLA v4 prefill ASM kernel for gfx1250
- [#4877](https://github.com/ROCm/aiter/pull/4877) Supports LSE in OPUS MHA for gfx950
- [#4866](https://github.com/ROCm/aiter/pull/4866) Moves Gluon gemm_a8w8 kernel into _gluon_kernels/gfx950
- [#4908](https://github.com/ROCm/aiter/pull/4908) Implements split-K for the FlyDSL a8w8 preshuffle GEMM
- [#4917](https://github.com/ROCm/aiter/pull/4917) Moves Gluon gemm_a8w8_blockscale kernel into _gluon_kernels
- [#4874](https://github.com/ROCm/aiter/pull/4874) Updates MHA CPP README
- [#4868](https://github.com/ROCm/aiter/pull/4868) Guards RDNA unified attention against LDS overflow
- [#4916](https://github.com/ROCm/aiter/pull/4916) Fixes ASM split-K semaphore deadlock under CUDA graph capture
- [#4878](https://github.com/ROCm/aiter/pull/4878) Disables Gluon for Triton fp4gemm on gfx1250
- [#4899](https://github.com/ROCm/aiter/pull/4899) Adds workload-aware KV-split count for MLA auto mode
- [#4925](https://github.com/ROCm/aiter/pull/4925) Skips fp4 silu_and_mul_quant tests on non-gfx950 architectures
- [#4880](https://github.com/ROCm/aiter/pull/4880) Fixes Paged Attention prefill performance regression for small HEAD_DIM
- [#4872](https://github.com/ROCm/aiter/pull/4872) Folds fp8 qlen 2 onto the qseqlen-4 kernel on gfx950
</details>

<details>
<summary>Performance (30)</summary>

- [#4749](https://github.com/ROCm/aiter/pull/4749) Tunes BF16 GEMM configurations
- [#4804](https://github.com/ROCm/aiter/pull/4804) Tunes BF16 GEMM for gfx1250 DeepSeek-V4-Flash shapes
- [#4851](https://github.com/ROCm/aiter/pull/4851) Adds gfx1250 A16W16 GEMM configs for FLUX.2 shapes
- [#4781](https://github.com/ROCm/aiter/pull/4781) Retunes small-M tiles and wave counts in the A16W16 fallback config for gfx950
- [#4718](https://github.com/ROCm/aiter/pull/4718) Tunes chunked_pa_prefill parameters for gfx950
- [#4632](https://github.com/ROCm/aiter/pull/4632) Tunes mla_decode_rope fp32 config for gfx950
- [#4915](https://github.com/ROCm/aiter/pull/4915) Drops gfx942/gfx950 opus rows from BF16 tuned-GEMM tables for Kimi K3
- [#4948](https://github.com/ROCm/aiter/pull/4948) Removes legacy flat-layout fallback from GEMM config resolution
- [#4947](https://github.com/ROCm/aiter/pull/4947) Unifies Gluon a8w8 blockscale config resolution
- [#4933](https://github.com/ROCm/aiter/pull/4933) Moves GEMM-AFP8WFP8_PRESHUFFLED configs to nested layout
- [#4918](https://github.com/ROCm/aiter/pull/4918) Retunes unified attention configs for gfx950
- [#4927](https://github.com/ROCm/aiter/pull/4927) Migrates a8w8 blockscale GEMM configs to nested layout
- [#4928](https://github.com/ROCm/aiter/pull/4928) Moves GEMM-A16W16-gated configs to nested layout
- [#4929](https://github.com/ROCm/aiter/pull/4929) Moves GEMM-A16W16-ATOMIC configs to nested layout
- [#4930](https://github.com/ROCm/aiter/pull/4930) Moves GEMM-A16W16 configs to nested layout
- [#4931](https://github.com/ROCm/aiter/pull/4931) Moves GEMM-A16W8_BLOCKSCALE family configs to nested layout
- [#4932](https://github.com/ROCm/aiter/pull/4932) Moves GEMM-A8WFP4 configs to nested layout
- [#4934](https://github.com/ROCm/aiter/pull/4934) Moves GEMM-A8W8_PER_TOKEN_SCALE configs to nested layout
- [#4935](https://github.com/ROCm/aiter/pull/4935) Moves GEMM-A8W8 configs to nested layout
- [#4936](https://github.com/ROCm/aiter/pull/4936) Moves GEMM-A16WFP4 and GEMM-A16WFP4_PRESHUFFLED configs to nested layout
- [#4937](https://github.com/ROCm/aiter/pull/4937) Moves FUSED-GEMM-AFP4WFP4-MUL_ADD configs to nested layout
- [#4938](https://github.com/ROCm/aiter/pull/4938) Moves FUSED-GEMM-AFP4WFP4-A16W16 family configs to nested layout
- [#4939](https://github.com/ROCm/aiter/pull/4939) Moves FUSED-GEMM-A8W8_BLOCKSCALE-MUL_ADD configs to nested layout
- [#4940](https://github.com/ROCm/aiter/pull/4940) Moves FUSED-GEMM-A8W8_BLOCKSCALE-A16W16 configs to nested layout
- [#4941](https://github.com/ROCm/aiter/pull/4941) Moves FF-A16W16-fused configs to nested layout
- [#4942](https://github.com/ROCm/aiter/pull/4942) Moves BATCHED_GEMM-AFP4WFP4 configs to nested layout
- [#4943](https://github.com/ROCm/aiter/pull/4943) Moves general configs to nested layout
- [#4944](https://github.com/ROCm/aiter/pull/4944) Moves BATCHED_GEMM-A8W8 configs to nested layout
- [#4945](https://github.com/ROCm/aiter/pull/4945) Moves BATCHED_GEMM-A16WFP4 configs to nested layout
- [#4946](https://github.com/ROCm/aiter/pull/4946) Moves BATCHED_GEMM-A16W16 configs to nested layout
</details>

<details>
<summary>Parallelism & scheduling (2)</summary>

- [#4832](https://github.com/ROCm/aiter/pull/4832) Integrates detorch fused_ar_mhc_post and pybind
- [#4924](https://github.com/ROCm/aiter/pull/4924) Fixes distributed raw IPC input pools and removes vestigial signal/buffer blocks
</details>

<details>
<summary>Tests, CI & build (13)</summary>

- [#4883](https://github.com/ROCm/aiter/pull/4883) Cherry-picks ROCm 10 hipcub fixes for release v0.1.20
- [#4895](https://github.com/ROCm/aiter/pull/4895) Enables GLM-5.2 and dynamic nodes in ATOM DI smoke tests
- [#4846](https://github.com/ROCm/aiter/pull/4846) Centralizes Docker login configuration
- [#4843](https://github.com/ROCm/aiter/pull/4843) Drops hipcub::Traits dependency to support ROCm 10 in sampling
- [#4697](https://github.com/ROCm/aiter/pull/4697) Covers int32 slot_mapping in test_kvcache
- [#4853](https://github.com/ROCm/aiter/pull/4853) Drops hipcub::Traits dependency to support ROCm 10 in topk_per_row
- [#4807](https://github.com/ROCm/aiter/pull/4807) Makes Aiter S3 wheel manifest cache-safe
- [#4842](https://github.com/ROCm/aiter/pull/4842) Temporarily skips dependency check in CI
- [#4897](https://github.com/ROCm/aiter/pull/4897) Adds Triton release test
- [#4857](https://github.com/ROCm/aiter/pull/4857) Adds Triton release test
- [#4905](https://github.com/ROCm/aiter/pull/4905) Uses upstream parallel scheduler for AOT builds
- [#4881](https://github.com/ROCm/aiter/pull/4881) Adds DCO signoff check to CI
- [#4912](https://github.com/ROCm/aiter/pull/4912) Bumps FlyDSL dependency to 0.3.2.dev838
</details>

<details>
<summary>Bugfixes (5)</summary>

- [#4825](https://github.com/ROCm/aiter/pull/4825) Fixes non-stage1 paged MQA logits for KV block size > 1 in DeepSeek V4
- [#4742](https://github.com/ROCm/aiter/pull/4742) Tolerates missing original_max_position_embeddings in RoPE
- [#4844](https://github.com/ROCm/aiter/pull/4844) Fixes MoE unit test OOM
- [#4841](https://github.com/ROCm/aiter/pull/4841) Adds acquire fence for mb radix barrier last block in topk
- [#4923](https://github.com/ROCm/aiter/pull/4923) Fixes MI300A gfx target in attention docs
</details>

<details>
<summary>Docs (1)</summary>

- [#4913](https://github.com/ROCm/aiter/pull/4913) Updates Copilot instructions
</details>

<details>
<summary>Other (3)</summary>

- [#4861](https://github.com/ROCm/aiter/pull/4861) Pins composable_kernel to 15e12dd7
- [#4870](https://github.com/ROCm/aiter/pull/4870) Adds validate-kernel-pr skill and structural D9 trigger for review-pr
- [#4896](https://github.com/ROCm/aiter/pull/4896) Submits minor updates for K3 SA
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: e3daa12ea2aa5acc513af77aa138e248c648cf42715109c5c2503216ee1e9c0f -->
