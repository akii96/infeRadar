# AITER: PR digest (2026-08-09 to 2026-08-13)

_62 merged, 47 newly opened - source ROCm/AITER, generated 2026-08-13T10:06:05Z_

## TL;DR
*   **Model Focus**: Heavy optimization for **Kimi** and **DeepSeek** (v4) architectures, specifically targeting MoE and MLA performance on next-generation AMD hardware (gfx950 and gfx1250).
*   **MoE & Quantization**: Massive leaps in MoE quantization pipelines, highlighted by the "megamoe" refactor, new Gluon A4W4 MoE kernels for gfx1250, and Opus FP8 mxscale BMMs for gfx950.
*   **Attention & MLA**: Significant attention improvements via new chunk delta attention Triton kernels, FlyDSL GDR reductions, and expanded MLA support (PS mode BF16/FP8, M-pack MTP regime).
*   **Framework Evolution**: Continued maturation of the FlyDSL and Gluon backends, alongside extensive Triton kernel tuning and efforts to de-torch C++ JIT components for lower overhead.

## Most important PRs
*   **[#4439](https://github.com/ROCm/aiter/pull/4439)** - Introduces the "megamoe" architecture, overhauling distributed MoE and quantization pipelines across FlyDSL and Python APIs to streamline communication and GEMM execution.
*   **[#4320](https://github.com/ROCm/aiter/pull/4320)** - Adds Opus FP8 mxscale batched matrix multiplication (BMM) kernels specifically tuned for gfx950, significantly boosting DeepSeek inference throughput.
*   **[#2513](https://github.com/ROCm/aiter/pull/2513)** - Implements a highly optimized Gluon MoE A4W4 kernel for gfx1250 using Triton, delivering major memory bandwidth savings for 4-bit weight quantized models.
*   **[#4679](https://github.com/ROCm/aiter/pull/4679)** (Newly opened) - Proposes a massive FlyDSL-based prefill GDN (Gated Delta Network) block implementation, aiming to drastically optimize prefill attention performance on AMD hardware.
*   **[#4668](https://github.com/ROCm/aiter/pull/4668)** (Newly opened) - Brings MHA batch mode and deep kernel optimizations to gfx1250 via FlyDSL, replacing over 7,000 lines of older implementation with a more efficient pipeline.

## More changes by area

<details>
<summary>Kernels & attention (26)</summary>

- [#4540](https://github.com/ROCm/aiter/pull/4540) Fix GDR reductions for FlyDSL 0.2.4
- [#4568](https://github.com/ROCm/aiter/pull/4568) Add chunk_delta_attn triton kernels for Kimi
- [#4353](https://github.com/ROCm/aiter/pull/4353) Add mfma16_hip GDR K5 prefill chunk_gdn_fwd_h for MI308
- [#4680](https://github.com/ROCm/aiter/pull/4680) Stop turning row/block numbers into 32-bit addresses and add direct-row SWA write
- [#4630](https://github.com/ROCm/aiter/pull/4630) Unify Triton loading and add a UT for configs
- [#4694](https://github.com/ROCm/aiter/pull/4694) Reuse GDN prefill metadata
- [#4572](https://github.com/ROCm/aiter/pull/4572) Add attn_res Triton kernel for K3
- [#4491](https://github.com/ROCm/aiter/pull/4491) Add gfx950 packed BF16 GDR decode kernel
- [#4415](https://github.com/ROCm/aiter/pull/4415) Implement length-adaptive deterministic top-k for sparse-MLA indexer
- [#4366](https://github.com/ROCm/aiter/pull/4366) Support fp32 chunk states in GDN prefill
- [#4671](https://github.com/ROCm/aiter/pull/4671) Fix LDS OOM issue on MI300 for Triton attention
- [#4523](https://github.com/ROCm/aiter/pull/4523) Enable chunk-gated-delta-rule-fwd-h on gfx1201
- [#4565](https://github.com/ROCm/aiter/pull/4565) Support mask0 in MI350 MLA PS mode BF16 case
- [#4657](https://github.com/ROCm/aiter/pull/4657) Add lse to fmha asm kernels for gfx950
- [#4440](https://github.com/ROCm/aiter/pull/4440) Support block sizes > 1 in paged MQA logits for DeepSeek v4
- [#4625](https://github.com/ROCm/aiter/pull/4625) Support 96-head 128-dim reduction in MLA
- [#4710](https://github.com/ROCm/aiter/pull/4710) Support 24-head 512-dim reduction in MLA
- [#4676](https://github.com/ROCm/aiter/pull/4676) (Newly opened) Implement fp8 unified attention for gfx950 via FlyDSL
- [#4645](https://github.com/ROCm/aiter/pull/4645) (Newly opened) Add FP8 D192/V128 prefill for Kimi on gfx942
- [#4706](https://github.com/ROCm/aiter/pull/4706) (Newly opened) Add 16mx8_32nx1_fp8fp8 opus kernel for MLA PS mode
- [#4683](https://github.com/ROCm/aiter/pull/4683) (Newly opened) Optimize chunk_delta_attn performance for Kimi
- [#4712](https://github.com/ROCm/aiter/pull/4712) (Newly opened) Add fused KDA decode kernel (conv1d + recurrence + gated RMSNorm)
- [#4726](https://github.com/ROCm/aiter/pull/4726) (Newly opened) Fuse block-banking cat into attn_res_gate
- [#4681](https://github.com/ROCm/aiter/pull/4681) (Newly opened) Add M-pack MTP regime (bh16mpack) for gfx950 MLA
- [#4698](https://github.com/ROCm/aiter/pull/4698) (Newly opened) Accept token-major w/u/g in opt-VK prefill state
- [#4727](https://github.com/ROCm/aiter/pull/4727) (Newly opened) Support 48-head 128-dim reduction in MLA
</details>

<details>
<summary>MoE & quantization (21)</summary>

- [#4646](https://github.com/ROCm/aiter/pull/4646) Port a16wi4 to new FlyDSL pipeline and clean old moe_gemm_2stage
- [#4714](https://github.com/ROCm/aiter/pull/4714) Add 8wave pipeline to a8w8 bpreshuffle gemm for Kimi
- [#4470](https://github.com/ROCm/aiter/pull/4470) Add more fine-grained tuning based on M for Gluon MoE
- [#4642](https://github.com/ROCm/aiter/pull/4642) Optimize MoE mxfp4 stage2 for gfx950
- [#4662](https://github.com/ROCm/aiter/pull/4662) Remove kpack from gfx950 MoE configs
- [#3093](https://github.com/ROCm/aiter/pull/3093) Add fused_mxfp4_quant for gfx1250
- [#4586](https://github.com/ROCm/aiter/pull/4586) Support sorted intermediate layout for opus_moe
- [#4170](https://github.com/ROCm/aiter/pull/4170) Implement GUGU act+quant fusion for MoE a8w4
- [#4613](https://github.com/ROCm/aiter/pull/4613) Add dtype dirs to the Triton/Gluon configs
- [#4693](https://github.com/ROCm/aiter/pull/4693) Add m<32 support for gfx1250 mxfp4
- [#4666](https://github.com/ROCm/aiter/pull/4666) Add DSv4 FP8/FP4 E=385/topk7 inter_dim=384 fused-MoE shape
- [#4670](https://github.com/ROCm/aiter/pull/4670) Use native FP4 conversion in MoE stage1 for FlyDSL
- [#4674](https://github.com/ROCm/aiter/pull/4674) Add optional inplace out buffer to gemm_a8w8_blockscale_bpreshuffle
- [#4652](https://github.com/ROCm/aiter/pull/4652) Add runtime-keyed Kimi-K3 A8W4 config
- [#4723](https://github.com/ROCm/aiter/pull/4723) (Newly opened) Unify A8W4 Stage2 with a runtime-K decode pipeline
- [#4730](https://github.com/ROCm/aiter/pull/4730) (Newly opened) Optimize MoE GEMM for gfx1250
- [#4655](https://github.com/ROCm/aiter/pull/4655) (Newly opened) Add support for v2 gemm2 a8w8
- [#4647](https://github.com/ROCm/aiter/pull/4647) (Newly opened) Reuse stage-1 scratch buffer across layers and graph captures
- [#4704](https://github.com/ROCm/aiter/pull/4704) (Newly opened) Add extern_moe_output param for combine zero-copy
- [#4688](https://github.com/ROCm/aiter/pull/4688) (Newly opened) Add sigmoid score_mode to the routing top-k
- [#4717](https://github.com/ROCm/aiter/pull/4717) (Newly opened) Avoid duplicate fp32 output alloc in torch_moe_stage2 reference
</details>

<details>
<summary>Performance & Tuning (6)</summary>

- [#4650](https://github.com/ROCm/aiter/pull/4650) Add gfx1250 96-head GEMM shapes to gptoss BF16 tuned config
- [#4479](https://github.com/ROCm/aiter/pull/4479) Tune Kimi-K3 prefill GEMMs for gfx950
- [#4664](https://github.com/ROCm/aiter/pull/4664) (Newly opened) Add gfx950 configs for three MI355X shapes in DSv4 a8w8 blockscale
- [#4648](https://github.com/ROCm/aiter/pull/4648) (Newly opened) Add gfx1100 A8W8 tuning config
- [#4663](https://github.com/ROCm/aiter/pull/4663) (Newly opened) Add gfx950 LM-head GEMM configs for DSv4 bf16
- [#4718](https://github.com/ROCm/aiter/pull/4718) (Newly opened) Tune chunked_pa_prefill params for gfx950
</details>

<details>
<summary>API, Framework & Refactors (16)</summary>

- [#4654](https://github.com/ROCm/aiter/pull/4654) Refactor and remove torch dependency from module_ropes
- [#4594](https://github.com/ROCm/aiter/pull/4594) Clean rocprim/hipcub in hip kernels
- [#4702](https://github.com/ROCm/aiter/pull/4702) De-torch topk_per_row / topk_plain and externalize workspaces
- [#4590](https://github.com/ROCm/aiter/pull/4590) Refactor and detorch module_aiter_unary
- [#4555](https://github.com/ROCm/aiter/pull/4555) Implement stage2 logits block load
- [#4578](https://github.com/ROCm/aiter/pull/4578) Swap gfx950 kernel to hold 64-bit memory addresses
- [#4729](https://github.com/ROCm/aiter/pull/4729) (Newly opened) Refactor and remove torch from module_mla_metadata
- [#4659](https://github.com/ROCm/aiter/pull/4659) (Newly opened) Add two fused ops for diffusion transformer blocks
- [#4651](https://github.com/ROCm/aiter/pull/4651) (Newly opened) Use shared runtime GPU architecture detection in JIT
- [#4686](https://github.com/ROCm/aiter/pull/4686) (Newly opened) Harden the C++ JIT loader (no shell, validated paths, trusted dlopen)
- [#4656](https://github.com/ROCm/aiter/pull/4656) (Newly opened) Remove sort for decode GDR
- [#4719](https://github.com/ROCm/aiter/pull/4719) (Newly opened) Tile q heads in fused_qk_rope_reshape_and_cache for gfx950
- [#4724](https://github.com/ROCm/aiter/pull/4724) (Newly opened) Remove in-C++ scratch allocation for fused_qk_norm_rope_cache_quant
- [#4715](https://github.com/ROCm/aiter/pull/4715) (Newly opened) Make semaphore/signal workspace CUDA-graph-capture safe for split-K hgemm
- [#4653](https://github.com/ROCm/aiter/pull/4653) (Newly opened) Default missing deepseek_yarn original_max_position_embeddings instead of raising
- [#4708](https://github.com/ROCm/aiter/pull/4708) (Newly opened) Support LoongArch64
</details>

<details>
<summary>Bugfixes (23)</summary>

- [#4621](https://github.com/ROCm/aiter/pull/4621) Fix CUDA graph mode error when PyTorch sets expandable_segments:True
- [#4494](https://github.com/ROCm/aiter/pull/4494) Fix ASM split-K semaphore deadlock under CUDA graph capture
- [#4709](https://github.com/ROCm/aiter/pull/4709) Revert "Fix ASM split-K semaphore deadlock under CUDA graph capture"
- [#4660](https://github.com/ROCm/aiter/pull/4660) Fix GPU arch detection logic
- [#4639](https://github.com/ROCm/aiter/pull/4639) Fix hipify qualifier loss and std::min build failures
- [#4675](https://github.com/ROCm/aiter/pull/4675) Propagate flat_mode through fmoe_g1u1 dispatch
- [#4611](https://github.com/ROCm/aiter/pull/4611) Drop per-kernel compile log and silence false-positive mxmoe warning
- [#4711](https://github.com/ROCm/aiter/pull/4711) Fix NaN in MLA Gluon MTP decode by zeroing fully causal-masked KV splits
- [#4545](https://github.com/ROCm/aiter/pull/4545) Fix Triton cache flooding in `_fwd_kernel_stage2_asm`
- [#4725](https://github.com/ROCm/aiter/pull/4725) Add missing `<optional>` header in topk_plain_kernels.cu
- [#4705](https://github.com/ROCm/aiter/pull/4705) Restore RNG seed in test_fused_rms_quant to fix flaky CI
- [#4682](https://github.com/ROCm/aiter/pull/4682) Fix causal fmha f8 hd256 kernel to return missing diagonal pairing
- [#4707](https://github.com/ROCm/aiter/pull/4707) (Newly opened) Stabilize SiTUv2 AOT cache keys in FlyDSL
- [#4691](https://github.com/ROCm/aiter/pull/4691) (Newly opened) Fix Gluon API compatibility for GFX12
- [#4690](https://github.com/ROCm/aiter/pull/4690) (Newly opened) Fix two OOB reads in fused_fp4_bmm_rope when EVEN_K is false
- [#4689](https://github.com/ROCm/aiter/pull/4689) (Newly opened) Mask the b_scales load in gemm_a16wfp4 when EVEN_K is false
- [#4673](https://github.com/ROCm/aiter/pull/4673) (Newly opened) Fix sparse decode gathering zeros from a strided cache
- [#4685](https://github.com/ROCm/aiter/pull/4685) (Newly opened) Fix two OOB reads in batched_gemm_a16wfp4 when EVEN_K is false
- [#4687](https://github.com/ROCm/aiter/pull/4687) (Newly opened) Fix epilogue store masks for cu_start != 0 in fp8_mqa_logits
- [#4716](https://github.com/ROCm/aiter/pull/4716) (Newly opened) Skip CK batch-prefill paged-KV OOB fault cell
- [#4696](https://github.com/ROCm/aiter/pull/4696) (Newly opened) Fix multi-rank JIT import race for on-demand modules
- [#4731](https://github.com/ROCm/aiter/pull/4731) (Newly opened) Fix fp8 mqa for DSv4 on gfx1250
- [#4713](https://github.com/ROCm/aiter/pull/4713) (Newly opened) Fix get_block_n_fp8 KeyError on speculative-decode verify widths
</details>

<details>
<summary>CI, Build & Docs (12)</summary>

- [#4619](https://github.com/ROCm/aiter/pull/4619) Run vLLM disagg from upstream main in CI
- [#3596](https://github.com/ROCm/aiter/pull/3596) Add FFM Triton test workflow
- [#4722](https://github.com/ROCm/aiter/pull/4722) Publish per-case vLLM DI accuracy and enable Kimi in CI
- [#4728](https://github.com/ROCm/aiter/pull/4728) Restore default GitHub Pages docs deployment
- [#4721](https://github.com/ROCm/aiter/pull/4721) Restore Triton split history for defaulted files
- [#4684](https://github.com/ROCm/aiter/pull/4684) Bump dawidd6/action-download-artifact to v21
- [#4678](https://github.com/ROCm/aiter/pull/4678) Add CODEOWNERS for aiter/ops/triton
- [#4700](https://github.com/ROCm/aiter/pull/4700) Revert "Add CODEOWNERS for aiter/ops/triton"
- [#4720](https://github.com/ROCm/aiter/pull/4720) (Newly opened) Add Copilot review instructions and modify README
- [#4649](https://github.com/ROCm/aiter/pull/4649) (Newly opened) Auto-update split test FILE_TIMES
- [#4703](https://github.com/ROCm/aiter/pull/4703) (Newly opened) Make AITER prebuild thread count configurable
- [#4697](https://github.com/ROCm/aiter/pull/4697) (Newly opened) Cover int32 slot_mapping in test_kvcache
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 30b73106f005897a347648b6b9b8846bd985a0c2e5c6b0fd23ec7865600a12df -->
