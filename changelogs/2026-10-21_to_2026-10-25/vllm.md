# vllm: PR digest (2026-10-21 to 2026-10-25)

_308 merged, 534 newly opened - source vllm-project/vllm, generated 2026-10-25T23:22:40Z_

## TL;DR
- **DeepSeek-V4/V4.1 got the most label attention (55).** The bigger story is specialized "mono" or fused decode paths, with new model families (Kimi-K3, MiniMax-M3/M3.1, GLM-5.3, Muse Spark, Qwen3.8-Flash-Next) following the same pattern. Merged: DSv4.1-Flash on GB300 (`[#61868](https://github.com/vllm-project/vllm/pull/61868)`), DSv4-Pro on MI355X (`[#61482](https://github.com/vllm-project/vllm/pull/61482)`), Kimi-K3 on MI355X (`[#60683](https://github.com/vllm-project/vllm/pull/60683)`), MiniMax-M3 MXFP4 (`[#62712](https://github.com/vllm-project/vllm/pull/62712)`).
- **ROCm/MI355X is the main perf frontier.** It covers monokernel decode, MXFP4 and MXFP8 MoE and GEMM, and FlyDSL/Triton ports. RDNA3/4 and gfx1151 skinny-GEMM work is also landing, and a wave of new-model support is queued as open PRs.
- **Spec decode is active (102 labels).** Merged work includes XPress (`[#54448](https://github.com/vllm-project/vllm/pull/54448)`), DSpark/DFlash ModelOpt loading, and MRV2 drafting skips. Open work includes a remote/standalone-GPU draft stack (`[#63333](https://github.com/vllm-project/vllm/pull/63333)`, `[#63334](https://github.com/vllm-project/vllm/pull/63334)`, `[#63335](https://github.com/vllm-project/vllm/pull/63335)`), a GLM-5.3 MTP drafter (`[#63387](https://github.com/vllm-project/vllm/pull/63387)`), and DSpark kernels.
- **Direction:** model-specific fused decode, KV offload/connector hardening, the Rust frontend reaching Python parity, and cleanup. Open `[#63373](https://github.com/vllm-project/vllm/pull/63373)` removes Model Runner V1 entirely (23k lines deleted).

## Most important PRs
**[#61868](https://github.com/vllm-project/vllm/pull/61868) — DeepSeek-V4.1-Flash specialized decode on GB300.** Adds a dedicated decode path spanning attention, MoE, quantization and speculative decode on Blackwell Ultra. It is the headline NVIDIA latency work of the window.

**[#61482](https://github.com/vllm-project/vllm/pull/61482) — DSv4-Pro standalone mono decode layer on MI355X.** Fuses the whole decode layer into one standalone kernel path on AMD. It is the template reused for Kimi-K3 (`[#60683](https://github.com/vllm-project/vllm/pull/60683)`) and MiniMax-M3 (`[#62712](https://github.com/vllm-project/vllm/pull/62712)`).

**[#63045](https://github.com/vllm-project/vllm/pull/63045) — Kimi-K3 KDA RecoverSSM.** CuTe verify and commit kernels keep the recurrent-state records outside the KV cache. This makes speculative verify workable for linear-attention (KDA) hybrids.

**[#62366](https://github.com/vllm-project/vllm/pull/62366) — Fuse Beam's TP all-reduce with sandwich norms and MoE finalize.** Removes separate collective and norm launches per layer on NVIDIA, cutting TP decode latency.

**[#62622](https://github.com/vllm-project/vllm/pull/62622) — Muse Spark Open on ROCm.** A large (13k-line) new-model enablement that touches Triton attention, MoE, multimodal and speculative decode.

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#58509](https://github.com/vllm-project/vllm/pull/58509) HY4 preview perf boost on ROCm
- [#62101](https://github.com/vllm-project/vllm/pull/62101) Cohere2MoE attention/MoE dual stream, single TP all-reduce per layer, fused add+RMSNorm
- [#60834](https://github.com/vllm-project/vllm/pull/60834) Opt-in paged MXFP4 sparse indexer dense path for DeepSeek-V4 on ROCm
- [#61855](https://github.com/vllm-project/vllm/pull/61855) Triton port of the fused GDN MTP decode kernel on ROCm
- [#62843](https://github.com/vllm-project/vllm/pull/62843) GLM low-latency BF16 GEMM on SM107
- [#62102](https://github.com/vllm-project/vllm/pull/62102) Skip scale calculation in concat_and_cache_mla (1.2-3% TPOT gain)
- [#60644](https://github.com/vllm-project/vllm/pull/60644) Packed fp16 W4A16 prefill dequant for gfx1151
- [#62994](https://github.com/vllm-project/vllm/pull/62994) MonoKernel serves EAGLE3 verify steps for MiniMax-M3
- [#57909](https://github.com/vllm-project/vllm/pull/57909) MiniMax-M3 indexer context-parallel enablement on ROCm
- [#62745](https://github.com/vllm-project/vllm/pull/62745) mHC TileLang: skip Sinkhorn on non-finite padding rows
- [#62171](https://github.com/vllm-project/vllm/pull/62171) Size cooperative_topk single pass by row length
- [#60643](https://github.com/vllm-project/vllm/pull/60643) Fuse Gemma4Unified 2D posemb and batch image/video embedder
- [#58660](https://github.com/vllm-project/vllm/pull/58660) Share orjson responses across render and pooling
- [#62850](https://github.com/vllm-project/vllm/pull/62850), [#57101](https://github.com/vllm-project/vllm/pull/57101), [#62940](https://github.com/vllm-project/vllm/pull/62940), [#62698](https://github.com/vllm-project/vllm/pull/62698), [#62654](https://github.com/vllm-project/vllm/pull/62654), [#63495](https://github.com/vllm-project/vllm/pull/63495) Smaller perf wins: encoder cache free, Molmo2 pooling, DispatchPooler bypass, MRV2 staged writes, watermarking argmax, Clef metadata

</details>

<details>
<summary>Kernels & attention (8)</summary>

- [#62016](https://github.com/vllm-project/vllm/pull/62016) CPU GELU-tanh MoE, FP8 checkpoints, Gemma-4 INT8 TP=4
- [#59082](https://github.com/vllm-project/vllm/pull/59082) CPU long-context MTP attention scheduling on AMX
- [#60532](https://github.com/vllm-project/vllm/pull/60532) Decode FlashInfer spec queries with fa2 on pre-SM90
- [#57832](https://github.com/vllm-project/vllm/pull/57832) Context-parallel sparse lightning indexer (Triton, opt-in)
- [#60413](https://github.com/vllm-project/vllm/pull/60413) W4A8 int8-dot MXFP4 GEMV for RDNA3/3.5
- [#57481](https://github.com/vllm-project/vllm/pull/57481) Capture CUDA graphs with expandable segments off for AITER all-reduce
- [#62384](https://github.com/vllm-project/vllm/pull/62384) Decoder-side SWA bounded replay with APC for DSv4.1-Flash
- [#58743](https://github.com/vllm-project/vllm/pull/58743) BF16 KDA recurrent state for Kimi-K3 on ROCm

</details>

<details>
<summary>MoE & quantization (8)</summary>

- [#63125](https://github.com/vllm-project/vllm/pull/63125) Quark MXFP8 W8A8 routed experts
- [#52780](https://github.com/vllm-project/vllm/pull/52780) Simulated routing in monolithic MoE backends
- [#57092](https://github.com/vllm-project/vllm/pull/57092) Batch-invariant online FP8 MoE experts
- [#62054](https://github.com/vllm-project/vllm/pull/62054) Sorted fused-MoE path for host-resident experts
- [#62751](https://github.com/vllm-project/vllm/pull/62751) Honor MoE activation override for Humming MXFP4
- [#62405](https://github.com/vllm-project/vllm/pull/62405) Use replace_parameter in process_weights_after_loading
- [#62907](https://github.com/vllm-project/vllm/pull/62907) MXFP4 SWIGLUOAI_UNINTERLEAVE test coverage on MI355
- [#63131](https://github.com/vllm-project/vllm/pull/63131) Validate gfx942 int4 expert requant for Kimi-K3

</details>

<details>
<summary>Model support (12)</summary>

- [#62938](https://github.com/vllm-project/vllm/pull/62938) Flint
- [#61651](https://github.com/vllm-project/vllm/pull/61651) Nemotron Parse 3.5 serving and MTP
- [#60149](https://github.com/vllm-project/vllm/pull/60149) Dory
- [#63095](https://github.com/vllm-project/vllm/pull/63095) MiniCPM-OCR 1.0
- [#62957](https://github.com/vllm-project/vllm/pull/62957) Alpamayo 2 Super
- [#62544](https://github.com/vllm-project/vllm/pull/62544) Domyn Edge
- [#62498](https://github.com/vllm-project/vllm/pull/62498) LoRA for Step5
- [#61391](https://github.com/vllm-project/vllm/pull/61391) LoRA for BERT token classification heads
- [#62194](https://github.com/vllm-project/vllm/pull/62194) NemotronHMTP shares target embedding and LM head
- [#62757](https://github.com/vllm-project/vllm/pull/62757) Muse Spark shares one RoPE cache
- [#63145](https://github.com/vllm-project/vllm/pull/63145) Real-valued RoPE in compiled Pixtral ViT
- [#62573](https://github.com/vllm-project/vllm/pull/62573) EPD metadata-only audio-in-video

</details>

<details>
<summary>Parallelism & scheduling (11)</summary>

- [#54448](https://github.com/vllm-project/vllm/pull/54448) XPress speculative decoding
- [#63001](https://github.com/vllm-project/vllm/pull/63001) Load ModelOpt mixed-precision DFlash/DSpark drafts
- [#58466](https://github.com/vllm-project/vllm/pull/58466) Adaptive verification in batch-sharded sampling
- [#62784](https://github.com/vllm-project/vllm/pull/62784) Skip drafting when no request can use drafts
- [#63251](https://github.com/vllm-project/vllm/pull/63251) Keep drafters within rotary cache on V2 runner
- [#61791](https://github.com/vllm-project/vllm/pull/61791) UMBP shared lookup, transfer, hybrid, observability
- [#61655](https://github.com/vllm-project/vllm/pull/61655) Migrate FlashInfer NVLink one-sided to MoEEpCommunication
- [#62366](https://github.com/vllm-project/vllm/pull/62366) see above for the Beam fusion
- [#59266](https://github.com/vllm-project/vllm/pull/59266) Enable WideEP EP16/DP16 tests on ROCm
- [#60028](https://github.com/vllm-project/vllm/pull/60028) Start multiproc workers concurrently under spawn
- [#55700](https://github.com/vllm-project/vllm/pull/55700) Watchdog for engine and worker monitoring

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#62419](https://github.com/vllm-project/vllm/pull/62419) Enable kernel/sampler unit tests on Intel XPU
- [#62014](https://github.com/vllm-project/vllm/pull/62014) Route multimodal prefix masks through Triton/FlashAttention on XPU
- [#62683](https://github.com/vllm-project/vllm/pull/62683) XPU prefix-caching tests for GDN, Mamba and pooling
- [#60298](https://github.com/vllm-project/vllm/pull/60298) Unit tests on Rubin
- [#63017](https://github.com/vllm-project/vllm/pull/63017) Pluggable layer for ViT mrope preparation

</details>

<details>
<summary>API & serving (22)</summary>

- [#62416](https://github.com/vllm-project/vllm/pull/62416), [#62826](https://github.com/vllm-project/vllm/pull/62826), [#62741](https://github.com/vllm-project/vllm/pull/62741), [#62825](https://github.com/vllm-project/vllm/pull/62825), [#63318](https://github.com/vllm-project/vllm/pull/63318) Rust frontend flags: tokenizer, histogram buckets, exclude-tools, stats interval, token-ids
- [#62874](https://github.com/vllm-project/vllm/pull/62874), [#62875](https://github.com/vllm-project/vllm/pull/62875), [#62892](https://github.com/vllm-project/vllm/pull/62892), [#62872](https://github.com/vllm-project/vllm/pull/62872), [#63062](https://github.com/vllm-project/vllm/pull/63062), [#63317](https://github.com/vllm-project/vllm/pull/63317), [#63316](https://github.com/vllm-project/vllm/pull/63316), [#63315](https://github.com/vllm-project/vllm/pull/63315), [#62824](https://github.com/vllm-project/vllm/pull/62824), [#62823](https://github.com/vllm-project/vllm/pull/62823), [#63313](https://github.com/vllm-project/vllm/pull/63313), [#63314](https://github.com/vllm-project/vllm/pull/63314), [#63059](https://github.com/vllm-project/vllm/pull/63059), [#59854](https://github.com/vllm-project/vllm/pull/59854), [#62721](https://github.com/vllm-project/vllm/pull/62721) Rust frontend parity: token-identity matching of parser markers, tool parsers, Mooncake metrics, bad words, logit_bias, and more
- [#60082](https://github.com/vllm-project/vllm/pull/60082) Derender output mode for generate
- [#63148](https://github.com/vllm-project/vllm/pull/63148) Share non-streaming chat message assembly with batch derender
- [#62706](https://github.com/vllm-project/vllm/pull/62706) Share ChatStreamProcessor between streaming and derender
- [#61772](https://github.com/vllm-project/vllm/pull/61772) Late chunking via /v1/embeddings
- [#62765](https://github.com/vllm-project/vllm/pull/62765) Prompt embeds for reasoning traces
- [#63088](https://github.com/vllm-project/vllm/pull/63088) Daemon-to-daemon warmup cache seeding for Preload
- [#55809](https://github.com/vllm-project/vllm/pull/55809) Save server queue time and TTFT in bench
- [#51974](https://github.com/vllm-project/vllm/pull/51974) profile_prefix in /start_profile
- [#63613](https://github.com/vllm-project/vllm/pull/63613) PCP support in vllm bench forward
- [#47112](https://github.com/vllm-project/vllm/pull/47112) Enforce max_tool_calls for Responses built-in tools
- [#62738](https://github.com/vllm-project/vllm/pull/62738) Use VLLMValidationError in renderers base
- [#62786](https://github.com/vllm-project/vllm/pull/62786) Harmony rendering in /tokenize

</details>

<details>
<summary>Bugfixes (47)</summary>

- [#62473](https://github.com/vllm-project/vllm/pull/62473), [#60808](https://github.com/vllm-project/vllm/pull/60808) MoRIIO READ fixes
- [#61019](https://github.com/vllm-project/vllm/pull/61019) OffloadingConnector partial tails with EAGLE/MTP
- [#56430](https://github.com/vllm-project/vllm/pull/56430) KV block leak under fault tolerance in P/D
- [#62591](https://github.com/vllm-project/vllm/pull/62591) Retain routed experts while a KV tier holds their blocks
- [#52921](https://github.com/vllm-project/vllm/pull/52921) Align CPU offload pool size across PP/spec-decode
- [#63120](https://github.com/vllm-project/vllm/pull/63120) DeepSeek-VL2 cache identity
- [#62692](https://github.com/vllm-project/vllm/pull/62692) Engram tables on CPU in the InstantTensor loader
- [#62719](https://github.com/vllm-project/vllm/pull/62719) Stop strings/tokens on derender
- [#61984](https://github.com/vllm-project/vllm/pull/61984) Anthropic thinking effort
- [#62294](https://github.com/vllm-project/vllm/pull/62294) Anthropic error types
- [#63345](https://github.com/vllm-project/vllm/pull/63345) Batch tool_choice rules for streamed tool calls
- [#59223](https://github.com/vllm-project/vllm/pull/59223) FP8 indexer WK pairs across load_weights
- [#62164](https://github.com/vllm-project/vllm/pull/62164) Multimodal sender-cache race
- [#62555](https://github.com/vllm-project/vllm/pull/62555) Cross-stream reuse of NCCL receive buffers
- [#59855](https://github.com/vllm-project/vllm/pull/59855), [#61780](https://github.com/vllm-project/vllm/pull/61780), [#63266](https://github.com/vllm-project/vllm/pull/63266), [#60810](https://github.com/vllm-project/vllm/pull/60810), [#61390](https://github.com/vllm-project/vllm/pull/61390) KV offload fixes
- [#63118](https://github.com/vllm-project/vllm/pull/63118) cooperative_topk NaN illegal access
- [#59717](https://github.com/vllm-project/vllm/pull/59717) moe_permute invalid topk_ids
- [#61749](https://github.com/vllm-project/vllm/pull/61749) Exact strides for moe_forward ops
- [#58304](https://github.com/vllm-project/vllm/pull/58304) FA4 FP8 descale strides
- [#62403](https://github.com/vllm-project/vllm/pull/62403) ROCm QK-norm+RoPE+KV fusion output
- [#63082](https://github.com/vllm-project/vllm/pull/63082) MiniMax-M3 IndexCache overrides
- [#63007](https://github.com/vllm-project/vllm/pull/63007) Engram hash gather across DP on AMD
- [#62652](https://github.com/vllm-project/vllm/pull/62652) DSv4.1 replay scoring rows
- [#63319](https://github.com/vllm-project/vllm/pull/63319) LoRA-wrapped MoE reloaded weights
- [#61196](https://github.com/vllm-project/vllm/pull/61196), [#60687](https://github.com/vllm-project/vllm/pull/60687) Gemma 4 placeholders and encoder CG
- [#62867](https://github.com/vllm-project/vllm/pull/62867), [#63339](https://github.com/vllm-project/vllm/pull/63339), [#63016](https://github.com/vllm-project/vllm/pull/63016), [#62665](https://github.com/vllm-project/vllm/pull/62665), [#48421](https://github.com/vllm-project/vllm/pull/48421) CPU: NUMA affinity, GDN conv-state, timeout, kv-cache dtype, LoRA bgmv
- [#62856](https://github.com/vllm-project/vllm/pull/62856), [#62928](https://github.com/vllm-project/vllm/pull/62928), [#62163](https://github.com/vllm-project/vllm/pull/62163), [#62783](https://github.com/vllm-project/vllm/pull/62783), [#62859](https://github.com/vllm-project/vllm/pull/62859), [#63112](https://github.com/vllm-project/vllm/pull/63112) Responses, beam score, derender logprobs, pooling
- [#62374](https://github.com/vllm-project/vllm/pull/62374) Rust frontend HTTP 500 on long conversations
- [#62583](https://github.com/vllm-project/vllm/pull/62583), [#63451](https://github.com/vllm-project/vllm/pull/63451) Fast Start daemon memory and cuBLAS workspaces
- [#60318](https://github.com/vllm-project/vllm/pull/60318), [#59941](https://github.com/vllm-project/vllm/pull/59941), [#62576](https://github.com/vllm-project/vllm/pull/62576), [#62884](https://github.com/vllm-project/vllm/pull/62884), [#62841](https://github.com/vllm-project/vllm/pull/62841), [#61509](https://github.com/vllm-project/vllm/pull/61509), [#63295](https://github.com/vllm-project/vllm/pull/63295), [#63190](https://github.com/vllm-project/vllm/pull/63190), [#62834](https://github.com/vllm-project/vllm/pull/62834), [#62880](https://github.com/vllm-project/vllm/pull/62880), [#57393](https://github.com/vllm-project/vllm/pull/57393), [#62099](https://github.com/vllm-project/vllm/pull/62099), [#63063](https://github.com/vllm-project/vllm/pull/63063) Misc fixes
- [#62977](https://github.com/vllm-project/vllm/pull/62977) plus 3 more minor fixes

</details>

<details>
<summary>Refactors (7)</summary>

- [#61649](https://github.com/vllm-project/vllm/pull/61649) Move FlyDSL UltraQuant/TurboQuant decode to public APIs
- [#63400](https://github.com/vllm-project/vllm/pull/63400) Remove dead code models
- [#56937](https://github.com/vllm-project/vllm/pull/56937) Unify mm prefix range computation
- [#63460](https://github.com/vllm-project/vllm/pull/63460) Share NCCL trainer rendezvous initialization
- [#62983](https://github.com/vllm-project/vllm/pull/62983) Revert parallel paged-attention build ([#62475](https://github.com/vllm-project/vllm/pull/62475))
- [#63013](https://github.com/vllm-project/vllm/pull/63013) Revert routed-expert capture hook ([#62624](https://github.com/vllm-project/vllm/pull/62624))
- [#62624](https://github.com/vllm-project/vllm/pull/62624) Platform hook for routed-expert capture rows (reverted)

</details>

<details>
<summary>Build & CI (15)</summary>

- [#63105](https://github.com/vllm-project/vllm/pull/63105) Reland paged attention kernel split (4-7x ROCm wheel build speedup)
- [#62475](https://github.com/vllm-project/vllm/pull/62475) Parallel paged attention compile (reverted)
- [#63609](https://github.com/vllm-project/vllm/pull/63609), [#63608](https://github.com/vllm-project/vllm/pull/63608) Disable CI jobs with unpinned or unlocked deps
- [#59100](https://github.com/vllm-project/vllm/pull/59100) Export kernel source maps for CI selection
- [#62934](https://github.com/vllm-project/vllm/pull/62934) Move NFS-affected MI300 groups to MI355
- [#62835](https://github.com/vllm-project/vllm/pull/62835) Refresh vulnerable runtime/test dependencies
- [#63413](https://github.com/vllm-project/vllm/pull/63413) Remove Ubuntu 24.04 release variant
- [#62883](https://github.com/vllm-project/vllm/pull/62883) Run 4xL4 steps nightly only
- [#61058](https://github.com/vllm-project/vllm/pull/61058) Fix Buildkite path filters
- [#63320](https://github.com/vllm-project/vllm/pull/63320) Run more server tests against the Rust frontend
- [#62816](https://github.com/vllm-project/vllm/pull/62816) Bump humming-kernels to 0.1.18
- [#63259](https://github.com/vllm-project/vllm/pull/63259) Recipe previews on push
- [#55901](https://github.com/vllm-project/vllm/pull/55901) Fix kv-B mypy errors
- [#62601](https://github.com/vllm-project/vllm/pull/62601) Raise the bar for agent-written tests

</details>

<details>
<summary>Docs (10)</summary>

- [#63552](https://github.com/vllm-project/vllm/pull/63552), [#63534](https://github.com/vllm-project/vllm/pull/63534), [#63222](https://github.com/vllm-project/vllm/pull/63222), [#63520](https://github.com/vllm-project/vllm/pull/63520), [#63395](https://github.com/vllm-project/vllm/pull/63395), [#63163](https://github.com/vllm-project/vllm/pull/63163) Kimi-K3 and MiniMax-M3 AgentX presets, recipes and profiles
- [#63236](https://github.com/vllm-project/vllm/pull/63236), [#63244](https://github.com/vllm-project/vllm/pull/63244), [#63428](https://github.com/vllm-project/vllm/pull/63428), [#63257](https://github.com/vllm-project/vllm/pull/63257) MiniMax-M3.1-Flash recipes (ROCm, Hopper FP8, GB200/GB300)
- [#61489](https://github.com/vllm-project/vllm/pull/61489) Point users at --disable-flashinfer-autotune
- [#63228](https://github.com/vllm-project/vllm/pull/63228) Fix griffe warnings in XPress kernels
- plus 1 more minor doc update

</details>

<details>
<summary>Other (3)</summary>

- [#56939](https://github.com/vllm-project/vllm/pull/56939) Mooncake transfer stats via Prometheus
- [#59703](https://github.com/vllm-project/vllm/pull/59703) Preserve group classification on placeholder KV events
- [#60774](https://github.com/vllm-project/vllm/pull/60774) Boolean sweep plot filters in benchmarks

</details>

<details>
<summary>Newly opened (in progress) highlights (20)</summary>

- [#63232](https://github.com/vllm-project/vllm/pull/63232) MiniMax-M3.1-Flash model support (36k lines)
- [#63387](https://github.com/vllm-project/vllm/pull/63387), [#63386](https://github.com/vllm-project/vllm/pull/63386), [#63102](https://github.com/vllm-project/vllm/pull/63102) GLM-5.3 MTP drafter, B200 CuTe latency decode, GB300 TP4 decode
- [#63373](https://github.com/vllm-project/vllm/pull/63373) Remove Model Runner V1
- [#63333](https://github.com/vllm-project/vllm/pull/63333), [#63334](https://github.com/vllm-project/vllm/pull/63334), [#63335](https://github.com/vllm-project/vllm/pull/63335) Remote and standalone-GPU draft placement with CUDA IPC transport
- [#63527](https://github.com/vllm-project/vllm/pull/63527), [#63246](https://github.com/vllm-project/vllm/pull/63246), [#63440](https://github.com/vllm-project/vllm/pull/63440) Muse Spark fp8 KV, TEP8 and FlyDSL DSpark verify monokernels
- [#63398](https://github.com/vllm-project/vllm/pull/63398) ATOM full-layer MiniMax-M3 MonoKernel
- [#63555](https://github.com/vllm-project/vllm/pull/63555), [#63032](https://github.com/vllm-project/vllm/pull/63032), [#63124](https://github.com/vllm-project/vllm/pull/63124) GLM-5.3-Flash and Qwen3.8-Flash-Next monokernels
- [#63381](https://github.com/vllm-project/vllm/pull/63381) DoSA prefill indexer on SM100
- [#63203](https://github.com/vllm-project/vllm/pull/63203) NVFP4 KV cache for dense MLA with FlashInfer
- [#63101](https://github.com/vllm-project/vllm/pull/63101) MXFP4 activation quant, 3x kernel speedup
- [#63040](https://github.com/vllm-project/vllm/pull/63040), [#63039](https://github.com/vllm-project/vllm/pull/63039), [#63273](https://github.com/vllm-project/vllm/pull/63273) TP8 MegaMoE for DeepSeek-V4, MiMo and K3 on ROCm
- [#62972](https://github.com/vllm-project/vllm/pull/62972) NIXL EP v2 elastic EP all2all
- [#63216](https://github.com/vllm-project/vllm/pull/63216), [#62853](https://github.com/vllm-project/vllm/pull/62853) RL NCCL M2N layouts and partitioned trainer groups
- [#63351](https://github.com/vllm-project/vllm/pull/63351), [#63350](https://github.com/vllm-project/vllm/pull/63350) Priority scheduling: prefill hold and KV-pressure preemption
- [#63406](https://github.com/vllm-project/vllm/pull/63406) Separate prefill and decode CUDA graph capture sizes
- [#63424](https://github.com/vllm-project/vllm/pull/63424) CPU FP8 MoE and native MXFP4 W4A8

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 16664ed9fb8b20958273ee8daa8cdeae94d008eab87182bc80b4260b625f3c61 -->
