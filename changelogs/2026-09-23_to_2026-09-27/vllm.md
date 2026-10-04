# vllm: PR digest (2026-09-23 to 2026-09-27)

_248 merged, 439 newly opened - source vllm-project/vllm, generated 2026-09-27T23:58:20Z_

## TL;DR
- **DeepSeek-V4/V4.1 got the most attention (43 labeled PRs).** Merged work fuses MoE finalize into the TP all-reduce (`[#58586](https://github.com/vllm-project/vllm/pull/58586)`), fuses inverse RoPE with FP8/MXFP8 quant into the sparse-MLA decode path (`[#58621](https://github.com/vllm-project/vllm/pull/58621)`, `[#58634](https://github.com/vllm-project/vllm/pull/58634)`), and adds ROCm equivalents (`[#58456](https://github.com/vllm-project/vllm/pull/58456)`, `[#57407](https://github.com/vllm-project/vllm/pull/57407)`). Qwen and Gemma got far less.
- **Fusion and removing host syncs were the main perf theme.** Examples: a low-SM multimem reduce-scatter on SM100/SM103 (`[#55072](https://github.com/vllm-project/vllm/pull/55072)`), TRTLLM-Gen top-k finalize deferral (`[#58635](https://github.com/vllm-project/vllm/pull/58635)`), a D2H-sync removal in FlashInfer sparse MLA (`[#58684](https://github.com/vllm-project/vllm/pull/58684)`), and FP8 quant kernel tuning (`[#55330](https://github.com/vllm-project/vllm/pull/55330)`, `[#58194](https://github.com/vllm-project/vllm/pull/58194)`).
- **ROCm/AMD was the most active hardware (132 PRs).** Work covered MXFP8 GEMM on gfx950 (`[#58510](https://github.com/vllm-project/vllm/pull/58510)`), QK-norm/RoPE/KV-cache fusion for MRoPE (`[#50212](https://github.com/vllm-project/vllm/pull/50212)`), and a large MI355 CI mirror effort.
- **Speculative decoding (73 PRs) is still evolving.** Merged work includes the LiLiCorr drafter (`[#57934](https://github.com/vllm-project/vllm/pull/57934)`), Gemma4 DSpark adaptive verification (`[#57263](https://github.com/vllm-project/vllm/pull/57263)`), and DCP targets with non-DCP DSpark (`[#56723](https://github.com/vllm-project/vllm/pull/56723)`). One DSpark PP change (`[#56956](https://github.com/vllm-project/vllm/pull/56956)`) was merged and then reverted (`[#58484](https://github.com/vllm-project/vllm/pull/58484)`).
- **Direction:** new-open work leans toward DSv4.1 on ROCm (paged MXFP4 indexer, a4w4 MoE default), a Rust frontend (Responses API, `n` choices), KV offload/connectors, and Qwen4Exp PLE storage.

## Most important PRs
**[#58586](https://github.com/vllm-project/vllm/pull/58586): DSV4.1 MoE finalize fused into the TP all-reduce + mHC boundary.** This removes a separate finalize pass and a kernel boundary on the DeepSeek V4.1 MoE path under TP, cutting launch and memory traffic.

**[#58621](https://github.com/vllm-project/vllm/pull/58621): Inverse RoPE + FP8 quant fused into FlashInfer sparse MLA (DSv4).** Output post-processing now runs inside the attention kernel, so the separate RoPE and quant passes are gone from the decode path.

**[#58634](https://github.com/vllm-project/vllm/pull/58634): DSv4.1 small-batch WO-A fused with inverse RoPE and MXFP8 quant (SM100/SM103).** This targets low-batch decode latency, where launch overhead dominates.

**[#55072](https://github.com/vllm-project/vllm/pull/55072): Low-SM multimem reduce-scatter for SM100/SM103.** It uses NVLink multimem collectives with few SMs, leaving more SMs free to overlap with compute.

**[#58510](https://github.com/vllm-project/vllm/pull/58510): MXFP8 GEMM on native 32x32 block scales for gfx950.** It runs MXFP8 GEMM directly on the hardware's block scales and credits the aiter kernels.

## More changes by area

<details>
<summary>Performance (23)</summary>

- [#50212](https://github.com/vllm-project/vllm/pull/50212) ROCm QK-norm/RoPE/KV-cache fusion extended to MRoPE
- [#58684](https://github.com/vllm-project/vllm/pull/58684) Remove D2H sync from FlashInfer SM90 sparse MLA plan under async scheduling
- [#55330](https://github.com/vllm-project/vllm/pull/55330) Register-resident path for per-token-group 8-bit quant
- [#58194](https://github.com/vllm-project/vllm/pull/58194) Vectorized flat abs-max for dynamic per-tensor FP8 quant
- [#58226](https://github.com/vllm-project/vllm/pull/58226) DiffusionGemma one-pass sampler statistics kernel
- [#58216](https://github.com/vllm-project/vllm/pull/58216) DiffusionGemma constrained reads over logprob_token_ids
- [#58720](https://github.com/vllm-project/vllm/pull/58720) Index expert mapping lookups in RoutedExperts.load_weights
- [#58880](https://github.com/vllm-project/vllm/pull/58880) Fused MiniMax2 routing with non-unit routed scaling
- [#58051](https://github.com/vllm-project/vllm/pull/58051) Skip top-k slots routed to non-local experts in the Triton experts path
- [#58450](https://github.com/vllm-project/vllm/pull/58450) GLM5.3 metadata op, 1.6-4.8x kernel-level speedup
- [#58582](https://github.com/vllm-project/vllm/pull/58582) Parallelize registered CUDA Triton kernel warmup at startup
- [#57586](https://github.com/vllm-project/vllm/pull/57586) Breakable CUDA graphs by default under VLLM_BATCH_INVARIANT
- [#49371](https://github.com/vllm-project/vllm/pull/49371) Batch Mamba2 prefill SSM state saves, removing GPU<->CPU syncs
- [#57214](https://github.com/vllm-project/vllm/pull/57214) Avoid blocking seq_lens D2H copy for pooling in FlashInfer metadata builder
- [#57918](https://github.com/vllm-project/vllm/pull/57918) Bound FlashInfer prefill dequantization scratch
- [#56067](https://github.com/vllm-project/vllm/pull/56067) Defer reasoning usage recounts for non-chat streams
- [#57528](https://github.com/vllm-project/vllm/pull/57528) Offload streaming derender detokenization
- [#58574](https://github.com/vllm-project/vllm/pull/58574) Lock-free histogram observations in Rust frontend
- [#56926](https://github.com/vllm-project/vllm/pull/56926) Serialize offloaded Engram lookups, pack host tables into huge pages
- [#58225](https://github.com/vllm-project/vllm/pull/58225) Narrow Triton prefill-attention KV tile on RDNA3/RDNA4
- [#53283](https://github.com/vllm-project/vllm/pull/53283) wvSplitK for single-output GEMMs on ROCm
- [#58527](https://github.com/vllm-project/vllm/pull/58527) Dispatch GEMM for Kimi-K3 vision patch embedder
- [#58512](https://github.com/vllm-project/vllm/pull/58512) Conv3dLayer for MiniMax-M3 patch embedding
- plus 2 more minor perf updates ([#58749](https://github.com/vllm-project/vllm/pull/58749), [#58526](https://github.com/vllm-project/vllm/pull/58526) covered under Kernels)

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#43048](https://github.com/vllm-project/vllm/pull/43048) Triton kernel dispatcher
- [#53175](https://github.com/vllm-project/vllm/pull/53175) Gemma4 FP8 KV FA4 head-dim 512 backend selection
- [#58069](https://github.com/vllm-project/vllm/pull/58069) Upgrade FlashInfer to 0.7.0
- [#58526](https://github.com/vllm-project/vllm/pull/58526) MiniMax-M3 triton_mrope for the vision tower, plus int64 offset fix
- [#54508](https://github.com/vllm-project/vllm/pull/54508) Zen CPU encoder attention on zentorch SDPA
- [#54967](https://github.com/vllm-project/vllm/pull/54967) zentorch SDPA for CPU MLA prefill
- [#56252](https://github.com/vllm-project/vllm/pull/56252) fp32 attention sinks on CPU
- [#53300](https://github.com/vllm-project/vllm/pull/53300) CPU GDN support for NIXL DS convolution-state layout
- [#54988](https://github.com/vllm-project/vllm/pull/54988) Layout-compatible backend for turboquant boundary layers on ROCm
- [#57451](https://github.com/vllm-project/vllm/pull/57451) ROCm DSv4 inverse RoPE fused into the sparse decode reduce
- [#58419](https://github.com/vllm-project/vllm/pull/58419) Fix TileLang mHC fused RMSNorm on 64-wide wavefronts

</details>

<details>
<summary>MoE & quantization (10)</summary>

- [#53585](https://github.com/vllm-project/vllm/pull/53585) Remove online quant in fp8.py in favor of online shorthands
- [#51800](https://github.com/vllm-project/vllm/pull/51800) Remove Quark-specific silent online quantization
- [#58427](https://github.com/vllm-project/vllm/pull/58427) Add Humming to the W4A8 MoE oracle
- [#46528](https://github.com/vllm-project/vllm/pull/46528) Humming wNaM asymmetric quant with compressed-tensors
- [#58201](https://github.com/vllm-project/vllm/pull/58201) VLLM_ROCM_USE_AITER_MOE_SITUV2 selects a4w4/a8w4/a16w4
- [#58234](https://github.com/vllm-project/vllm/pull/58234) GateLinear for all MoE models
- [#57176](https://github.com/vllm-project/vllm/pull/57176) Select per-token NVFP4 MoE backends explicitly
- [#57954](https://github.com/vllm-project/vllm/pull/57954) Refresh online NVFP4 scales before reload post-processing
- [#54223](https://github.com/vllm-project/vllm/pull/54223) Fix MXFP8 startup crash below mm_mxfp8 shape limits
- [#57071](https://github.com/vllm-project/vllm/pull/57071) AMD-Quark mixed-precision DeepSeek-V4.1 support

</details>

<details>
<summary>Model support (7)</summary>

- [#44229](https://github.com/vllm-project/vllm/pull/44229) DeepSeek-V4 FIM completion rendering
- [#55957](https://github.com/vllm-project/vllm/pull/55957) granite_thinking_parser reasoning parser for Granite 4.2
- [#49648](https://github.com/vllm-project/vllm/pull/49648) Migrate Granite tool parser to the streaming Parser Engine
- [#58046](https://github.com/vllm-project/vllm/pull/58046) Mypy typing for Qwen and Qianfan models
- [#58045](https://github.com/vllm-project/vllm/pull/58045) ROCm Kimi-K3 low-concurrency speculative KDA
- [#58499](https://github.com/vllm-project/vllm/pull/58499) Avoid host sync in DSV4.1 ViT CUDA graph replay metadata
- [#58316](https://github.com/vllm-project/vllm/pull/58316) Update DeepSeek V4.1 Flash reasoning effort mappings

</details>

<details>
<summary>Parallelism & scheduling (11)</summary>

- [#51520](https://github.com/vllm-project/vllm/pull/51520) Sharding-aware NCCL M2N weight transfer for RL
- [#57075](https://github.com/vllm-project/vllm/pull/57075) Prefill context parallelism with data parallelism
- [#56723](https://github.com/vllm-project/vllm/pull/56723) DCP target model with non-DCP DSpark
- [#56956](https://github.com/vllm-project/vllm/pull/56956) DSpark pipeline-parallel targets (merged, then reverted)
- [#58484](https://github.com/vllm-project/vllm/pull/58484) Revert of [#56956](https://github.com/vllm-project/vllm/pull/56956)
- [#58098](https://github.com/vllm-project/vllm/pull/58098) BF16 AsyncTP fusion on ROCm
- [#58473](https://github.com/vllm-project/vllm/pull/58473) Fix EPLB load statistics during scaling
- [#56377](https://github.com/vllm-project/vllm/pull/56377) Disable sequence parallelism/async TP under batch invariance
- [#58459](https://github.com/vllm-project/vllm/pull/58459) Tune --long-prefill-token-threshold adaptiveness
- [#58442](https://github.com/vllm-project/vllm/pull/58442) *(not shown in the merged list; open)* Avoid scheduler deadlocks under KV pressure
- [#57632](https://github.com/vllm-project/vllm/pull/57632) Capture DFlash context K/V precompute in the draft CUDA graph

</details>

<details>
<summary>Speculative decoding (6)</summary>

- [#57934](https://github.com/vllm-project/vllm/pull/57934) LiLiCorr drafter
- [#57263](https://github.com/vllm-project/vllm/pull/57263) Gemma4 DSpark adaptive verification with FlashInfer
- [#52988](https://github.com/vllm-project/vllm/pull/52988) Variable-length decode for Kimi-K3 adaptive verification
- [#57497](https://github.com/vllm-project/vllm/pull/57497) Qwen4Exp PLE n-gram table CPU offload
- [#54631](https://github.com/vllm-project/vllm/pull/54631) Separate DSpark width from MTP stage validation
- [#58863](https://github.com/vllm-project/vllm/pull/58863) Open: RecoverSSM for Qwen GDN and PLE short conv

</details>

<details>
<summary>Hardware & arch (6)</summary>

- [#55721](https://github.com/vllm-project/vllm/pull/55721) XPU SYCL apply_rotary_emb kernel
- [#51600](https://github.com/vllm-project/vllm/pull/51600) XPU graph enabled by default
- [#56013](https://github.com/vllm-project/vllm/pull/56013) XPU upgrade to PyTorch 2.14
- [#50605](https://github.com/vllm-project/vllm/pull/50605) ROCm torch 2.13 / triton 3.8 bump
- [#58140](https://github.com/vllm-project/vllm/pull/58140) CPU uses pre-built triton
- [#58133](https://github.com/vllm-project/vllm/pull/58133) Gate AVX10.2 paths on compiler support

</details>

<details>
<summary>API & serving (14)</summary>

- [#56680](https://github.com/vllm-project/vllm/pull/56680) `vllm preload` CLI for fast restart
- [#58552](https://github.com/vllm-project/vllm/pull/58552) /health endpoint for the weight cache daemon
- [#58370](https://github.com/vllm-project/vllm/pull/58370) Wait for weight cache daemon readiness
- [#56086](https://github.com/vllm-project/vllm/pull/56086) response_format + tool_choice=auto
- [#58613](https://github.com/vllm-project/vllm/pull/58613) Handle disabled thinking in /v1/messages
- [#58786](https://github.com/vllm-project/vllm/pull/58786) Anthropic thinking disabled with P/D
- [#58754](https://github.com/vllm-project/vllm/pull/58754) Detect Anthropic inline-system merge against the resolved template
- [#58830](https://github.com/vllm-project/vllm/pull/58830) Gate per-request multimodal processor kwargs
- [#57205](https://github.com/vllm-project/vllm/pull/57205) Console logging as CLI configuration
- [#58321](https://github.com/vllm-project/vllm/pull/58321) Native Lark grammar parsing in xgrammar backend
- [#58306](https://github.com/vllm-project/vllm/pull/58306) Rust frontend --sse-keep-alive-interval
- [#58311](https://github.com/vllm-project/vllm/pull/58311) Rust frontend custom chat roles
- [#58545](https://github.com/vllm-project/vllm/pull/58545) Remove slow tokenizer mode
- [#57251](https://github.com/vllm-project/vllm/pull/57251) Prometheus metrics for SimpleCPUOffloadConnector

</details>

<details>
<summary>Bugfixes (32)</summary>

- [#58454](https://github.com/vllm-project/vllm/pull/58454) GLM-5.3-Flash kpool corruption with spec decode
- [#58704](https://github.com/vllm-project/vllm/pull/58704) GLM-5.3-Flash SM90 sparse MLA index_kpool mismatch
- [#55528](https://github.com/vllm-project/vllm/pull/55528) Align packed block strides for V3.2 sparse MLA
- [#58215](https://github.com/vllm-project/vllm/pull/58215) Bound DeepSelect sentinel columns in sparse top-k remap
- [#55277](https://github.com/vllm-project/vllm/pull/55277) NoPE sparse MLA on FlashInfer SM120
- [#58430](https://github.com/vllm-project/vllm/pull/58430) Allocator fragmentation shrinking KV cache during profiling
- [#58275](https://github.com/vllm-project/vllm/pull/58275) Capture prefill kernels for mixed FULL graphs
- [#58434](https://github.com/vllm-project/vllm/pull/58434) Padded prompt tails as spec-decode rows for hybrid models
- [#58368](https://github.com/vllm-project/vllm/pull/58368) Mamba prompt-tail prefix-cache hits with MTP
- [#58612](https://github.com/vllm-project/vllm/pull/58612) Outlines EOS termination after rejected drafts
- [#58444](https://github.com/vllm-project/vllm/pull/58444) Standard linear metadata for LM heads
- [#58626](https://github.com/vllm-project/vllm/pull/58626) Count reasoning tokens for Harmony/DeepSeek-V3/Step3
- [#58372](https://github.com/vllm-project/vllm/pull/58372) Count Kimi K3 reasoning tokens
- [#58792](https://github.com/vllm-project/vllm/pull/58792) Inkling tool name leaking into content
- [#58583](https://github.com/vllm-project/vllm/pull/58583) Keep logprobs of parser-suppressed streaming chunks
- [#58551](https://github.com/vllm-project/vllm/pull/58551) Respect max_output_tokens in Harmony tool-call loop
- [#57241](https://github.com/vllm-project/vllm/pull/57241) Default missing detail for Responses API images
- [#46303](https://github.com/vllm-project/vllm/pull/46303) Keep length finish_reason for truncated streaming tool calls
- [#58488](https://github.com/vllm-project/vllm/pull/58488) Full logprobs in token-in/token-out responses
- [#50769](https://github.com/vllm-project/vllm/pull/50769) Apply penalties from override-generation-config
- [#57696](https://github.com/vllm-project/vllm/pull/57696) Reject encoder-cache hits with mismatched embedding counts
- [#51694](https://github.com/vllm-project/vllm/pull/51694) Incremental multimodal block hashing
- [#58288](https://github.com/vllm-project/vllm/pull/58288) Keep every multimodal feature in partial-block KV event
- [#52623](https://github.com/vllm-project/vllm/pull/52623) ovis2_5 multimodal tokens
- [#48419](https://github.com/vllm-project/vllm/pull/48419) allowed_token_ids_mask aliasing in swap_states
- [#43931](https://github.com/vllm-project/vllm/pull/43931) Clear stale allowed_token_ids mask in condense
- [#57988](https://github.com/vllm-project/vllm/pull/57988) Release prompt_embeds tensor when slot is freed
- [#49845](https://github.com/vllm-project/vllm/pull/49845) KV block size supported by every attention backend
- [#58489](https://github.com/vllm-project/vllm/pull/58489) Keep pinned PLE prefetch ids out of the CUDA graph pool
- [#58310](https://github.com/vllm-project/vllm/pull/58310) Reject offloaded Engram tables larger than host memory
- [#56168](https://github.com/vllm-project/vllm/pull/56168) CPU MoE OOB write with fp32 router weights
- plus 1 more minor fix ([#58212](https://github.com/vllm-project/vllm/pull/58212) VllmConfig re-validation for submodel views)

</details>

<details>
<summary>KV connectors & disaggregation (9)</summary>

- [#51681](https://github.com/vllm-project/vllm/pull/51681) Fix ROCm mori-io multi-decode P/D misrouting race
- [#50047](https://github.com/vllm-project/vllm/pull/50047) Release dead peer's NIXL state without waiting for TTL
- [#58188](https://github.com/vllm-project/vllm/pull/58188) Restore NIXL push completion reporting
- [#58292](https://github.com/vllm-project/vllm/pull/58292) Reap expired NIXL leases behind a heartbeated head
- [#58919](https://github.com/vllm-project/vllm/pull/58919) Retry Mooncake bootstrap registration on timeout
- [#58472](https://github.com/vllm-project/vllm/pull/58472) Fix DecodeBench fp8 fill values, add startup fill mode
- [#49300](https://github.com/vllm-project/vllm/pull/49300) Mooncake CUSTOM_MEM_POOL
- [#57775](https://github.com/vllm-project/vllm/pull/57775) Finalize saves on steps without a forward
- [#57453](https://github.com/vllm-project/vllm/pull/57453) Retain offload event metadata through batch translation

</details>

<details>
<summary>Tests (10)</summary>

- [#56809](https://github.com/vllm-project/vllm/pull/56809) Watermarking golden tests for backwards compatibility
- [#58393](https://github.com/vllm-project/vllm/pull/58393) Harden AITER MoE sorting-backend env-var test matrix
- [#58093](https://github.com/vllm-project/vllm/pull/58093) Cover MoRI graph replay and output lifetime
- [#58091](https://github.com/vllm-project/vllm/pull/58091) Check GDN prefill numerics and output ownership
- [#58740](https://github.com/vllm-project/vllm/pull/58740) Test AMD DeepSeek V4 MoE routing against PyTorch reference
- [#58724](https://github.com/vllm-project/vllm/pull/58724) Cover AITER MQA logits dispatch on gfx950
- [#55612](https://github.com/vllm-project/vllm/pull/55612) Cover chunked prefill in batch-invariance suite
- [#58342](https://github.com/vllm-project/vllm/pull/58342) Fix flaky sharded-sampling tests
- [#58701](https://github.com/vllm-project/vllm/pull/58701) Report subprocess test skips as skips
- [#58469](https://github.com/vllm-project/vllm/pull/58469) Share BF16 baselines across quantization comparison tests

</details>

<details>
<summary>CI & build (20)</summary>

- [#57599](https://github.com/vllm-project/vllm/pull/57599) Expand single-GPU coverage on MI355 DPX
- [#57054](https://github.com/vllm-project/vllm/pull/57054) Split Basic Correctness into named jobs
- [#57237](https://github.com/vllm-project/vllm/pull/57237) Split Spec Decode Speculators + MTP into 4 jobs
- [#58095](https://github.com/vllm-project/vllm/pull/58095) Validate Mooncake and NIXL P/D accuracy on ROCm
- [#58281](https://github.com/vllm-project/vllm/pull/58281) MI355 dense NVFP4 and MoRI kernel mirrors
- [#58558](https://github.com/vllm-project/vllm/pull/58558) Mirror DSv4-Flash disaggregated DP EP group on MI355
- [#58748](https://github.com/vllm-project/vllm/pull/58748) Quantized MoE serving test for gfx950
- [#58369](https://github.com/vllm-project/vllm/pull/58369) Fusion E2E TP2 Quick on MI355 plus AITER MLA fix
- [#58244](https://github.com/vllm-project/vllm/pull/58244) Fix CI runtime/tests for MI355 DPX
- [#58282](https://github.com/vllm-project/vllm/pull/58282) Mirror TurboQuant evaluation groups on MI355
- [#58432](https://github.com/vllm-project/vllm/pull/58432) MI355 TurboQuant t3nc mirror
- [#58012](https://github.com/vllm-project/vllm/pull/58012) MI355 Kimi-K3 unit test group
- [#50922](https://github.com/vllm-project/vllm/pull/50922) ROCm Stage G gating
- [#58628](https://github.com/vllm-project/vllm/pull/58628) Report to CRCR after all jobs finish
- plus 6 more minor CI updates

</details>

<details>
<summary>Refactors (7)</summary>

- [#58550](https://github.com/vllm-project/vllm/pull/58550) Transformers v5 names, drop redundant processor use_fast
- [#58803](https://github.com/vllm-project/vllm/pull/58803) Remove dead test utils
- [#58446](https://github.com/vllm-project/vllm/pull/58446) Remove dead or duplicate tests
- [#58572](https://github.com/vllm-project/vllm/pull/58572) Move auxiliary files out of repository root
- [#57980](https://github.com/vllm-project/vllm/pull/57980) MRV2 miscellaneous cleanup
- [#58610](https://github.com/vllm-project/vllm/pull/58610) MRV2 model_runner.py cleanup
- [#57732](https://github.com/vllm-project/vllm/pull/57732) Reusable pure functions for FP8 and MLA weight transforms

</details>

<details>
<summary>Other (5)</summary>

- [#58587](https://github.com/vllm-project/vllm/pull/58587) *(open)* per-model Humming LM Eval jobs
- [#58659](https://github.com/vllm-project/vllm/pull/58659) Credit ROCm/aiter for block32 GEMM kernel
- [#57634](https://github.com/vllm-project/vllm/pull/57634) Rust frontend vision preprocessing context for Nemotron-H
- [#58378](https://github.com/vllm-project/vllm/pull/58378) Prevent MM timing from enabling debug tracing
- plus 49 more small merged PRs not shown in the source list

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: b0ff00d9df570feb5ca85d7df7fd5e7992521c509cc064f46290800ef6aac068 -->
