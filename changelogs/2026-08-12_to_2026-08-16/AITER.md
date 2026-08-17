# AITER: PR digest (2026-08-12 to 2026-08-16)

_59 merged, 50 newly opened - source ROCm/AITER, generated 2026-08-16T21:23:35Z_

## TL;DR

*   **Model Focus:** DeepSeek and Kimi dominated the window, with heavy optimization targeting AMD's gfx950 and gfx1250 architectures.
*   **Quantization & MoE:** A massive push on low-bit quantization (FP8, MXFP4, A4W4, A8W4) and MoE kernels, leveraging both Gluon and FlyDSL backends for extreme throughput.
*   **Attention & MLA:** Significant attention improvements, including new MLA (Multi-Head Latent Attention) kernels for DeepSeek and fused GDN prefill kernels for Kimi.
*   **Frameworks & Architecture:** Ongoing migration to Triton and FlyDSL, alongside efforts to decouple core C++ kernels from PyTorch (`detorch`) to reduce overhead.

## Most important PRs

*   **[#4320](https://github.com/ROCm/aiter/pull/4320)** Add opus fp8 mxscale BMM kernels for gfx950
    Delivers a massive FP8 block-scaled matrix multiplication kernel for DeepSeek on gfx950, significantly boosting throughput.
*   **[#4246](https://github.com/ROCm/aiter/pull/4246)** gfx1250 opus gemm splitk fuse
    Fuses split-K GEMM operations for DeepSeek and Kimi on gfx1250, reducing kernel launch overhead and improving memory bandwidth utilization.
*   **[#2513](https://github.com/ROCm/aiter/pull/2513)** [TRITON] [GLUON] GFX1250 Gluon MoE A4W4 Kernel
    Introduces a highly optimized A4W4 MoE kernel via the Gluon backend for gfx1250, critical for running heavily quantized models.
*   **[#4598](https://github.com/ROCm/aiter/pull/4598)** [Perf][FlyDSL] Add gdn_prepare: a fused intra-chunk GDN prefill prepare kernel
    Fuses the GDN prefill preparation step into a single kernel via FlyDSL, yielding a major performance win for attention prefill.
*   **[#4747](https://github.com/ROCm/aiter/pull/4747)** Fp8 mxscale bmm bpreshuffle opt
    An in-progress, massive optimization for FP8 BMM with block preshuffling on gfx950, aimed at further accelerating DeepSeek.

## More changes by area

<details>
<summary>MoE & quantization (19)</summary>

- [#4646](https://github.com/ROCm/aiter/pull/4646) ports a16wi4 to the new FlyDSL pipeline and cleans up old moe_gemm_2stage
- [#4723](https://github.com/ROCm/aiter/pull/4723) unifies A8W4 Stage2 with a runtime-K decode pipeline
- [#4562](https://github.com/ROCm/aiter/pull/4562) adds multicast support for MoE a8w4 on gfx1250 via Gluon
- [#4642](https://github.com/ROCm/aiter/pull/4642) optimizes MoE mxfp4 stage2 for gfx950 in FlyDSL
- [#4757](https://github.com/ROCm/aiter/pull/4757) adds a mori HIP dispatch backend for mega_moe
- [#4693](https://github.com/ROCm/aiter/pull/4693) adds m<32 support for gfx1250 mxfp4 in Triton
- [#4670](https://github.com/ROCm/aiter/pull/4670) uses native FP4 conversion in MoE stage1 for FlyDSL
- [#4674](https://github.com/ROCm/aiter/pull/4674) adds an optional inplace out buffer to gemm_a8w8_blockscale_bpreshuffle
- [#4717](https://github.com/ROCm/aiter/pull/4717) avoids duplicate fp32 output allocation in torch_moe_stage2 reference
- [#4746](https://github.com/ROCm/aiter/pull/4746) adds a parameter for combine quant
- [#4764](https://github.com/ROCm/aiter/pull/4764) maps FP8 to torch.float8_e4m3fn on RDNA3
- [#4785](https://github.com/ROCm/aiter/pull/4785) (Opened) implements mega stage2 for gfx1250
- [#4755](https://github.com/ROCm/aiter/pull/4755) (Opened) unifies A8W4 metadata and runtime dispatch for Opus MoE
- [#4730](https://github.com/ROCm/aiter/pull/4730) (Opened) optimizes MoE GEMM for gfx1250
- [#4748](https://github.com/ROCm/aiter/pull/4748) (Opened) fixes asm gemm corner cases and adds a_preshuffle=0 f4gemm & f8gemm for gfx1250
- [#4782](https://github.com/ROCm/aiter/pull/4782) (Opened) adds direct dense A4W4 MXFP4 GEMM for gfx950 in FlyDSL
- [#4772](https://github.com/ROCm/aiter/pull/4772) (Opened) adds dense BF16 x MXFP4 GEMM for gfx950 in FlyDSL
- [#4762](https://github.com/ROCm/aiter/pull/4762) (Opened) consumes prepared stage1 activation scales in MoE
- [#4704](https://github.com/ROCm/aiter/pull/4704) (Opened) adds extern_moe_output parameter for combine zero-copy in fmoe

</details>

<details>
<summary>Kernels & attention (16)</summary>

- [#4706](https://github.com/ROCm/aiter/pull/4706) adds 16mx8_32nx1_fp8fp8 opus kernel for MLA PS mode, increasing performance by 3-8%
- [#4729](https://github.com/ROCm/aiter/pull/4729) refactors module_mla_metadata and removes torch dependencies
- [#4572](https://github.com/ROCm/aiter/pull/4572) adds attn_res kernel for K3 in Triton
- [#4473](https://github.com/ROCm/aiter/pull/4473) adds Opus hd192 hybrid buffer path for large KV (>4GiB)
- [#4450](https://github.com/ROCm/aiter/pull/4450) relocates MLA Gluon kernel and unifies decode dispatch for GFX950
- [#4555](https://github.com/ROCm/aiter/pull/4555) implements stage2 logits block load for MLA
- [#4741](https://github.com/ROCm/aiter/pull/4741) (Opened) adds gfx950 Kimi Delta Attention prefill kernel in FlyDSL
- [#4732](https://github.com/ROCm/aiter/pull/4732) (Opened) supports prefill GDN K5 fp32 chunk states in FlyDSL
- [#4771](https://github.com/ROCm/aiter/pull/4771) (Opened) adds fused paged-prefill kernel for page_size=1, head_dim 64/256 in Triton FMHA
- [#4766](https://github.com/ROCm/aiter/pull/4766) (Opened) implements sparse MLA training backward for GFX950 DSV4 in Triton Gluon
- [#4712](https://github.com/ROCm/aiter/pull/4712) (Opened) adds fused KDA decode kernel (conv1d + recurrence + gated RMSNorm)
- [#4726](https://github.com/ROCm/aiter/pull/4726) (Opened) fuses block-banking cat into attn_res_gate via close_block/WRITE_BLOCK
- [#4784](https://github.com/ROCm/aiter/pull/4784) (Opened) supports causal=False (msk0 kernels) for MI350 MLA BF16/FP8 decode
- [#4698](https://github.com/ROCm/aiter/pull/4698) (Opened) accepts token-major w/u/g in opt-VK prefill state for Triton GDN
- [#4775](https://github.com/ROCm/aiter/pull/4775) (Opened) exposes paged MQA SplitKV override
- [#4758](https://github.com/ROCm/aiter/pull/4758) (Opened) implements deeper async-copy pipeline in the bh16 stage-1 decode loop for Gluon MLA

</details>

<details>
<summary>Performance & tuning (16)</summary>

- [#4683](https://github.com/ROCm/aiter/pull/4683) optimizes chunk_delta_attn performance in Triton
- [#4714](https://github.com/ROCm/aiter/pull/4714) adds 8wave pipeline to a8w8 bpreshuffle gemm for MI355
- [#4470](https://github.com/ROCm/aiter/pull/4470) adds more fine-grained tuning based on M for Gluon
- [#4719](https://github.com/ROCm/aiter/pull/4719) optimizes fused_qk_rope_reshape_and_cache kernel for gfx950
- [#4749](https://github.com/ROCm/aiter/pull/4749) (Opened) tunes bf16 gemm for DeepSeek on gfx1250
- [#4773](https://github.com/ROCm/aiter/pull/4773) (Opened) tunes mxfp8 gemm for GFX12 in Triton Gluon
- [#4776](https://github.com/ROCm/aiter/pull/4776) (Opened) chunks the non-FP4 gather_kv_b_proj over KV for MLA performance
- [#4761](https://github.com/ROCm/aiter/pull/4761) (Opened) optimizes Triton unified attention prefill and decode
- [#4736](https://github.com/ROCm/aiter/pull/4736) (Opened) replaces block_ptr in HSTU attn kernel
- [#4760](https://github.com/ROCm/aiter/pull/4760) (Opened) updates a8w8 gemm tuned config for gfx1250 in FlyDSL
- [#4767](https://github.com/ROCm/aiter/pull/4767) (Opened) adds MXFP4 fused-MoE configs for gfx950 (TP8) for Qwen3.8
- [#4778](https://github.com/ROCm/aiter/pull/4778) (Opened) enables RDNA3 in arch allow-list and adds Triton GEMM A8W8 tuning config
- [#4759](https://github.com/ROCm/aiter/pull/4759) (Opened) adds full 16-tier Qwen3-VL FP4 MoE tuned config for gfx950
- [#4781](https://github.com/ROCm/aiter/pull/4781) (Opened) retunes small-M tiles and wave counts in the A16W16 fallback config for gfx950
- [#4718](https://github.com/ROCm/aiter/pull/4718) (Opened) tunes chunked_pa_prefill params for gfx950
- [#4733](https://github.com/ROCm/aiter/pull/4733) (Opened) improves hd256 fp8 attention performance

</details>

<details>
<summary>Refactors & architecture (8)</summary>

- [#4694](https://github.com/ROCm/aiter/pull/4694) reuses GDN prefill metadata
- [#4594](https://github.com/ROCm/aiter/pull/4594) cleans rocprim/hipcub in hip kernels
- [#4702](https://github.com/ROCm/aiter/pull/4702) de-torches topk_per_row / topk_plain and externalizes workspaces
- [#4724](https://github.com/ROCm/aiter/pull/4724) removes in-C++ scratch allocation from fused_qk_norm_rope_cache_quant
- [#4739](https://github.com/ROCm/aiter/pull/4739) (Opened) hardens AITER_ASM_DIR code-object loading
- [#4708](https://github.com/ROCm/aiter/pull/4708) (Opened) adds support for LoongArch64
- [#4756](https://github.com/ROCm/aiter/pull/4756) (Opened) removes vestigial py_itfs_common.h includes and makes top_k_per_row torch-free
- [#4715](https://github.com/ROCm/aiter/pull/4715) (Opened) makes semaphore/signal workspace CUDA-graph-capture safe for FlyDSL split-K hgemm

</details>

<details>
<summary>Bugfixes (22)</summary>

- [#4671](https://github.com/ROCm/aiter/pull/4671) fixes LDS OOM issue on MI300 in Triton
- [#4621](https://github.com/ROCm/aiter/pull/4621) fixes car graph mode error when pytorch sets expandable_segments:True
- [#4494](https://github.com/ROCm/aiter/pull/4494) fixes ASM split-K semaphore deadlock under CUDA graph capture
- [#4709](https://github.com/ROCm/aiter/pull/4709) reverts the ASM split-K semaphore deadlock fix
- [#4774](https://github.com/ROCm/aiter/pull/4774) fixes 32-bit KV block offsets in gluon paged-MQA logits kernel
- [#4673](https://github.com/ROCm/aiter/pull/4673) fixes sparse decode gathering zeros from a strided cache in Triton
- [#4530](https://github.com/ROCm/aiter/pull/4530) fixes memory access fault in Triton MOE routing
- [#4777](https://github.com/ROCm/aiter/pull/4777) uses __align__ instead of alignas after __shared__ in opus_gemm
- [#4711](https://github.com/ROCm/aiter/pull/4711) fixes NaN in MLA Gluon MTP decode by zeroing fully causal-masked KV splits
- [#4545](https://github.com/ROCm/aiter/pull/4545) fixes Triton cache flooding in _fwd_kernel_stage2_asm
- [#4725](https://github.com/ROCm/aiter/pull/4725) adds missing <optional> header in topk_plain_kernels.cu
- [#4705](https://github.com/ROCm/aiter/pull/4705) restores RNG seed in test_fused_rms_quant to fix flaky mxfp4 quant CI
- [#4682](https://github.com/ROCm/aiter/pull/4682) fixes causal fmha f8 hd256 kernel to return missing diagonal pairing
- [#4707](https://github.com/ROCm/aiter/pull/4707) (Opened) stabilizes SiTUv2 AOT cache keys in FlyDSL
- [#4740](https://github.com/ROCm/aiter/pull/4740) (Opened) fixes gfx1201 bf16 g1u1 small m moe
- [#4779](https://github.com/ROCm/aiter/pull/4779) (Opened) handles GroupNorm autocast safely
- [#4742](https://github.com/ROCm/aiter/pull/4742) (Opened) tolerates missing original_max_position_embeddings in rope
- [#4716](https://github.com/ROCm/aiter/pull/4716) (Opened) skips CK batch-prefill paged-KV OOB fault cell
- [#4753](https://github.com/ROCm/aiter/pull/4753) (Opened) fixes LL proto ar dispatch
- [#4731](https://github.com/ROCm/aiter/pull/4731) (Opened) fixes fp8 mqa for dsv4 on gfx1250
- [#4786](https://github.com/ROCm/aiter/pull/4786) (Opened) uses SYSTEM scope + ACQUIRE ordering for cross-device signal loads in custom_all_reduce
- [#4713](https://github.com/ROCm/aiter/pull/4713) (Opened) fixes get_block_n_fp8 KeyError on speculative-decode verify widths for MLA fp8

</details>

<details>
<summary>CI, tests & docs (23)</summary>

- [#4561](https://github.com/ROCm/aiter/pull/4561) fixes ISA kernel optimization guide and example scripts
- [#4619](https://github.com/ROCm/aiter/pull/4619) runs vLLM disagg from upstream main in CI
- [#4720](https://github.com/ROCm/aiter/pull/4720) adds copilot review instructions and modifies readme file for Triton
- [#4366](https://github.com/ROCm/aiter/pull/4366) supports fp32 chunk states in GDN prefill tests
- [#4649](https://github.com/ROCm/aiter/pull/4649) auto-updates split test FILE_TIMES in CI
- [#3596](https://github.com/ROCm/aiter/pull/3596) adds FFM Triton test workflow
- [#4418](https://github.com/ROCm/aiter/pull/4418) adds always-run Aiter test gate
- [#4722](https://github.com/ROCm/aiter/pull/4722) publishes per-case vLLM DI accuracy and enables Kimi in CI
- [#4728](https://github.com/ROCm/aiter/pull/4728) restores default GitHub Pages docs deployment
- [#4721](https://github.com/ROCm/aiter/pull/4721) restores Triton split history for defaulted files
- [#4744](https://github.com/ROCm/aiter/pull/4744) pins PyTorch test image
- [#4734](https://github.com/ROCm/aiter/pull/4734) skips Triton test suites on docs-only changes
- [#4678](https://github.com/ROCm/aiter/pull/4678) adds CODEOWNERS for aiter/ops/triton
- [#4700](https://github.com/ROCm/aiter/pull/4700) reverts the addition of CODEOWNERS for aiter/ops/triton
- [#4727](https://github.com/ROCm/aiter/pull/4727) supports 48-head 128-dim reduction in MLA tests
- [#4710](https://github.com/ROCm/aiter/pull/4710) supports 24-head 512-dim reduction in MLA tests
- [#4688](https://github.com/ROCm/aiter/pull/4688) adds sigmoid score_mode to the routing top-k in Triton moe tests
- [#4750](https://github.com/ROCm/aiter/pull/4750) (Opened) centralizes PyTorch test image config
- [#4737](https://github.com/ROCm/aiter/pull/4737) (Opened) adds PR auto tag workflow
- [#4703](https://github.com/ROCm/aiter/pull/4703) (Opened) makes AITER prebuild thread count configurable
- [#4738](https://github.com/ROCm/aiter/pull/4738) (Opened) makes RNG deterministic in KV cache unit test
- [#4754](https://github.com/ROCm/aiter/pull/4754) (Opened) disables cpp_itfs sampling on ROCm 10
- [#4768](https://github.com/ROCm/aiter/pull/4768) (Opened) includes headers necessary for ROCm 10.0.0

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 6931f34506367ed93390d5f9b93452db761db2c7dcce1f1384ee7ccdbaeab35c -->
