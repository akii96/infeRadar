# vllm: PR digest (2026-09-16 to 2026-09-20)

_271 merged, 452 newly opened - source vllm-project/vllm, generated 2026-09-20T23:19:36Z_

## TL;DR
- **DeepSeek V4/V4.1 dominated the window.** Merged work covered the FlashMLA mega-attention backend with an NVFP4 compressed KV cache, DeepGEMM Mega-Gate, MegaMoE padding and staging, and encoder CUDA graphs. Several ROCm fixes and perf items also landed (FP8 WO_A projection, HCA dual-stream overlap, decode metadata reuse).
- **Perf work spanned kernels and memory.** Merged: Humming quant integration with shared Marlin/Humming workspaces, CPU FP8 W8A8 linear/MoE, Arm paged-attention rework, GLM-5.3-Flash kpool Triton fusion, a 3 GiB decode-workspace saving, and ROCm AITER QuickReduce+RMSNorm fusion.
- **Open work is mostly DSv4.1 and ROCm kernel fusion.** In-flight items include FP4/NVFP4 compressed-KV paths on gfx950, a fused wo_b GEMM with sequence-parallel reduce-scatter, TP all-reduce fused with mHC, and Kimi-K3 MoE/MLA kernels. CPU backends for Qwen3.8-Flash-Next and GLM5Next are also open.
- **Direction:** a hardening push on KV offload/connectors (NIXL, Mooncake, MoRIIO), the Rust frontend, and the ruff docstring and Transformers 5.17 migration. A large RL cluster of attention-sink `weight_loader` fixes is open.

## Most important PRs
**[#56935](https://github.com/vllm-project/vllm/pull/56935) DSv4.1 FlashMLA mega attention and NVFP4 compressed KV cache.** Adds a mega-attention path and an NVFP4-compressed KV cache for DeepSeek V4.1 on NVIDIA and AMD. This cuts KV memory and bandwidth for long contexts.

**[#56685](https://github.com/vllm-project/vllm/pull/56685) Humming feature integration.** Integrates the Humming quantized GEMM/MoE kernels. Follow-up [#57421](https://github.com/vllm-project/vllm/pull/57421) shares persistent workspaces between Marlin and Humming to cut memory.

**[#49942](https://github.com/vllm-project/vllm/pull/49942) CPU FP8 W8A8 linear/MoE support.** Brings FP8 W8A8 linear and MoE layers to CPU, widening quantized-MoE serving beyond GPUs. [#56985](https://github.com/vllm-project/vllm/pull/56985) adds a per-tensor FP8 W8A16 kernel for Ministral.

**[#52101](https://github.com/vllm-project/vllm/pull/52101) MoonEP BF16 balanced-EP backend.** Adds a new expert-parallel dispatch/combine backend aimed at router-imbalance load. A benchmark against DeepEP-HT is open in [#57598](https://github.com/vllm-project/vllm/pull/57598).

**[#51052](https://github.com/vllm-project/vllm/pull/51052) MoRIIO transfer of hybrid mamba/KDA recurrent state in READ mode.** Lets P/D disaggregation move recurrent state, not just KV, for hybrid models. A K3 DSpark hybrid READ follow-up is open in [#57700](https://github.com/vllm-project/vllm/pull/57700).

## More changes by area

<details>
<summary>Performance (22)</summary>

- [#57204](https://github.com/vllm-project/vllm/pull/57204) remove MegaMoE padding and shared-expert padding workaround on DSV4.1
- [#57604](https://github.com/vllm-project/vllm/pull/57604) optimize MegaMoE staging and NVFP4 cache gathers
- [#56568](https://github.com/vllm-project/vllm/pull/56568) pad shared experts for native MegaMoE fusion
- [#54674](https://github.com/vllm-project/vllm/pull/54674) stack DeepSeek V4 context WKV projections for DSpark
- [#56441](https://github.com/vllm-project/vllm/pull/56441) KV-only context insertion across V4.1 cache formats for DSpark
- [#57534](https://github.com/vllm-project/vllm/pull/57534) fuse GLM kpool tail slot mapping into one Triton kernel
- [#57327](https://github.com/vllm-project/vllm/pull/57327) cooperative top-k for small GLM decode batches
- [#57701](https://github.com/vllm-project/vllm/pull/57701) size GLM-5 sparse indexer decode workspace (3072 MiB saved)
- [#57456](https://github.com/vllm-project/vllm/pull/57456) sm_120 tuned configs for batch-invariant persistent matmul
- [#57273](https://github.com/vllm-project/vllm/pull/57273) sm_90 tuning table for Qwen4Exp QSA
- [#56045](https://github.com/vllm-project/vllm/pull/56045) refactor paged attention for Arm CPUs
- [#55960](https://github.com/vllm-project/vllm/pull/55960) fused DFlash2 grouped convolution
- [#55190](https://github.com/vllm-project/vllm/pull/55190) fuse CohereASR relative attention score accumulation
- [#57095](https://github.com/vllm-project/vllm/pull/57095) batch image requests per encoder in EPD
- [#48249](https://github.com/vllm-project/vllm/pull/48249) AITER QuickReduce + RMSNorm fusion on ROCm
- [#53623](https://github.com/vllm-project/vllm/pull/53623) AITER GDN decode fast path for flat qkvz layouts
- [#56849](https://github.com/vllm-project/vllm/pull/56849) MiniMax-M3 sparse-PA K/V insert without a contiguous copy
- [#54894](https://github.com/vllm-project/vllm/pull/54894) FP8 WO_A output projection for ROCm DSV4
- [#56853](https://github.com/vllm-project/vllm/pull/56853) HCA dual-stream overlap for DSV4 on ROCm
- [#57434](https://github.com/vllm-project/vllm/pull/57434) reuse decode topk ragged metadata across layers on ROCm
- [#57229](https://github.com/vllm-project/vllm/pull/57229) reduce CUDA graph divergences on ROCm
- [#57355](https://github.com/vllm-project/vllm/pull/57355) fix max-load throughput cliff when max_num_seqs is not a multiple of 8

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#57546](https://github.com/vllm-project/vllm/pull/57546) route GLM kpool indexer top-k through shared SparseIndexerTopk dispatcher
- [#55358](https://github.com/vllm-project/vllm/pull/55358) move sparse_attn_indexer_kpool into model folder, split AMD/NVIDIA
- [#51065](https://github.com/vllm-project/vllm/pull/51065) TritonMLA illegal memory access on causal multi-token decode
- [#53864](https://github.com/vllm-project/vllm/pull/53864) CuteDSL BF16 KKT inversion divergence in GDN
- [#56902](https://github.com/vllm-project/vllm/pull/56902) release stale FlashMLA workspace views after growth
- [#57575](https://github.com/vllm-project/vllm/pull/57575) reserve sparse prefill buffers before KV cache sizing
- [#51367](https://github.com/vllm-project/vllm/pull/51367) Murmur3 RNG for Gumbel sampling
- [#57377](https://github.com/vllm-project/vllm/pull/57377) pad activation scales to a multiple of 4 for C3x SM100 FP8 blockwise
- [#56538](https://github.com/vllm-project/vllm/pull/56538) expose effective attention block size for DCP
- [#49435](https://github.com/vllm-project/vllm/pull/49435) fix SM100 fp8_ds_mla cache scales
- [#57621](https://github.com/vllm-project/vllm/pull/57621) remove dead kernel code

</details>

<details>
<summary>MoE & quantization (13)</summary>

- [#48606](https://github.com/vllm-project/vllm/pull/48606) native Quark W4A16 INT4/UINT4 exports
- [#55316](https://github.com/vllm-project/vllm/pull/55316) W8A8 INT8 MoE on POWER
- [#55867](https://github.com/vllm-project/vllm/pull/55867) FP8 TP with FlashInfer TRTLLM MoE for Qwen3.8-Flash-Next
- [#54699](https://github.com/vllm-project/vllm/pull/54699) convert FlashInfer BF16 MoE weights in place
- [#57405](https://github.com/vllm-project/vllm/pull/57405) encapsulate TRT-LLM BF16 weight layout handling
- [#55934](https://github.com/vllm-project/vllm/pull/55934) triton_kernels 3.8 mxfp4 MoE on ROCm (gpt-oss, DSV4)
- [#53940](https://github.com/vllm-project/vllm/pull/53940) a4w4 flydsl kernels for Kimi-K3 on ROCm
- [#53162](https://github.com/vllm-project/vllm/pull/53162) int8_w8a8 MoE on Triton for XPU
- [#56079](https://github.com/vllm-project/vllm/pull/56079) skip SP padded rows in grouped MoE routing
- [#53914](https://github.com/vllm-project/vllm/pull/53914) DeepGEMM FP8 workspace over-allocation
- [#57316](https://github.com/vllm-project/vllm/pull/57316) ModelOpt MXFP8 layers load pre-processed weights
- [#57784](https://github.com/vllm-project/vllm/pull/57784) bf16 MoE router and mxfp4 MoE for MiMo V2
- [#57426](https://github.com/vllm-project/vllm/pull/57426) gate AITER MXFP8 MoE on the aiter enable flag
- plus 4 more minor ROCm MoE/quant fixes ([#56590](https://github.com/vllm-project/vllm/pull/56590), [#56359](https://github.com/vllm-project/vllm/pull/56359), [#57055](https://github.com/vllm-project/vllm/pull/57055), [#54248](https://github.com/vllm-project/vllm/pull/54248))

</details>

<details>
<summary>Model support (14)</summary>

- [#56227](https://github.com/vllm-project/vllm/pull/56227) encoder-side SWA-bounded replay for DeepSeek-V4.1-Flash
- [#56625](https://github.com/vllm-project/vllm/pull/56625) encoder CUDA graph for DeepSeek-V4.1-Flash
- [#56266](https://github.com/vllm-project/vllm/pull/56266) integrate Mega-Gate from DeepGEMM for DSv4.1
- [#57152](https://github.com/vllm-project/vllm/pull/57152) restore causal image SWA for DSV4.1
- [#57432](https://github.com/vllm-project/vllm/pull/57432) fix FlashInfer DSpark non-causal attention
- [#57454](https://github.com/vllm-project/vllm/pull/57454) preserve NaN-scored candidate block indices on DSv4.1
- [#55557](https://github.com/vllm-project/vllm/pull/55557) Qwen4Exp fp8_e4m3 main KV cache on QSA
- [#57508](https://github.com/vllm-project/vllm/pull/57508) fix MiMo-V2.5 fused fp8 qkv_proj sharding
- [#57487](https://github.com/vllm-project/vllm/pull/57487) fix Aria expert weight names/layout
- [#55911](https://github.com/vllm-project/vllm/pull/55911) Gemma4 loads weights with AutoWeightsLoader
- [#56231](https://github.com/vllm-project/vllm/pull/56231) LoRA for Nemotron VL language model
- [#49819](https://github.com/vllm-project/vllm/pull/49819) Cohere2MoE Eagle3 aux hidden states
- [#57563](https://github.com/vllm-project/vllm/pull/57563) Mistral-Large-3 accuracy regression
- [#56034](https://github.com/vllm-project/vllm/pull/56034) Sarvam MLA routing with FP32 router logits

</details>

<details>
<summary>Parallelism & scheduling (11)</summary>

- [#56497](https://github.com/vllm-project/vllm/pull/56497) Model Runner V2 custom logits processors
- [#56758](https://github.com/vllm-project/vllm/pull/56758) add --max-num-active-seqs to cap RUNNING admission
- [#53936](https://github.com/vllm-project/vllm/pull/53936) atomic admission for parallel sampling (n>1)
- [#44987](https://github.com/vllm-project/vllm/pull/44987) XPU EPLB
- [#56930](https://github.com/vllm-project/vllm/pull/56930) fix EAGLE and dense draft startup with EP
- [#57270](https://github.com/vllm-project/vllm/pull/57270) route dummy tokens to MoE experts during MRV2 profiling
- [#56456](https://github.com/vllm-project/vllm/pull/56456) match fast-prefill padding to active LoRA batches in MRV2
- [#55055](https://github.com/vllm-project/vllm/pull/55055) fix multi-layer MTP KV caches during P/D with MRV2
- [#57050](https://github.com/vllm-project/vllm/pull/57050) fix Mamba block allocation estimate blocking admission
- [#57104](https://github.com/vllm-project/vllm/pull/57104) fix deadlock with KVConnector + MTP under KV pressure
- [#57226](https://github.com/vllm-project/vllm/pull/57226) avoid blocking collective RPC during engine handshake

</details>

<details>
<summary>KV cache, offload & connectors (27)</summary>

- [#50045](https://github.com/vllm-project/vllm/pull/50045) back-pressure detection and remediation for KV offloading
- [#51787](https://github.com/vllm-project/vllm/pull/51787) track cache recency once per request
- [#51081](https://github.com/vllm-project/vllm/pull/51081) register the offload region in chunks
- [#54014](https://github.com/vllm-project/vllm/pull/54014) check cgroup memory before SHM allocation
- [#55885](https://github.com/vllm-project/vllm/pull/55885) per-request max_load_tokens control
- [#56709](https://github.com/vllm-project/vllm/pull/56709) restore MTP-retained sliding-window history
- [#56799](https://github.com/vllm-project/vllm/pull/56799) compact canonical MLA rows
- [#56810](https://github.com/vllm-project/vllm/pull/56810) skip non-prefix-cacheable groups in SimpleCPUOffload
- [#57145](https://github.com/vllm-project/vllm/pull/57145) skip scratch groups in kv_offload
- [#57160](https://github.com/vllm-project/vllm/pull/57160) private pinned tensors for CPU KV offload on ROCm
- [#56855](https://github.com/vllm-project/vllm/pull/56855) report request-level KV load failures under HMA in Mooncake
- [#56242](https://github.com/vllm-project/vllm/pull/56242) cross-encoder caching in Mooncake P2P
- [#54176](https://github.com/vllm-project/vllm/pull/54176) dynamic EPD proxy
- [#54960](https://github.com/vllm-project/vllm/pull/54960) EC Connector metrics
- [#55854](https://github.com/vllm-project/vllm/pull/55854) separate NIXL transport-failure metrics from KV expiry
- [#57570](https://github.com/vllm-project/vllm/pull/57570) avoid NIXL receive reports for notification-only requests
- [#57049](https://github.com/vllm-project/vllm/pull/57049) HiSparse/NIXL import full blocks without tail prefill on D
- [#57077](https://github.com/vllm-project/vllm/pull/57077) HiSparse/PD align region-mapped pulls across block sizes
- [#56841](https://github.com/vllm-project/vllm/pull/56841) make ExampleHiddenStatesConnector abort-safe
- [#55844](https://github.com/vllm-project/vllm/pull/55844) bind KV-event publishers at port 0
- [#56925](https://github.com/vllm-project/vllm/pull/56925) restore KV cache metadata GET method
- [#54222](https://github.com/vllm-project/vllm/pull/54222) report prefill worker cache hits in prompt_tokens_details
- [#57317](https://github.com/vllm-project/vllm/pull/57317) disable slot mapping kernel for GLM kpool tail
- [#57068](https://github.com/vllm-project/vllm/pull/57068) fix np.float64 leaking into KV transfer metrics log
- [#57477](https://github.com/vllm-project/vllm/pull/57477) address kpool tail blocks by padded indexer stride
- [#54990](https://github.com/vllm-project/vllm/pull/54990) skip 0.0% prefix-cache hit-rate log before any query
- [#56950](https://github.com/vllm-project/vllm/pull/56950) DP index for dense DP weight updates and EC CPU region

</details>

<details>
<summary>Hardware & arch (13)</summary>

- [#56985](https://github.com/vllm-project/vllm/pull/56985) CPU per-tensor FP8 W8A16 kernel for Ministral
- [#54923](https://github.com/vllm-project/vllm/pull/54923) fall back to CpuPlatform when zentorch fails
- [#56015](https://github.com/vllm-project/vllm/pull/56015) honor device_ids for XPU worker placement
- [#55953](https://github.com/vllm-project/vllm/pull/55953) Rubin CUDA 13.4 nightly images
- [#57132](https://github.com/vllm-project/vllm/pull/57132) revert two ROCm changes to fix DeepSeek-V4 accuracy
- [#50455](https://github.com/vllm-project/vllm/pull/50455) ROCm DSV4 sparse-indexer logits collapse on gfx950/gfx942
- [#56176](https://github.com/vllm-project/vllm/pull/56176) GLM-5.3-Flash Quark MXFP4 checkpoint on ROCm
- [#56726](https://github.com/vllm-project/vllm/pull/56726) ignore descales for unquantized AITER caches
- [#55991](https://github.com/vllm-project/vllm/pull/55991) skip AITER norm kernels when flattening would copy
- [#57074](https://github.com/vllm-project/vllm/pull/57074) AITER FP8/unquantized cases in modular-kernel sweep, MoRI per-tensor FP8 dispatch fix
- [#57192](https://github.com/vllm-project/vllm/pull/57192) apply deferred tilelang.jit on attribute access
- [#57425](https://github.com/vllm-project/vllm/pull/57425) alias SparseAttnIndexerKpool.forward_cuda to forward_native
- [#53674](https://github.com/vllm-project/vllm/pull/53674) MiniMax-M3 fused MXFP8 block scale on ROCm

</details>

<details>
<summary>API & serving (19)</summary>

- [#50550](https://github.com/vllm-project/vllm/pull/50550) stream reasoning and tool calls from the derender endpoint
- [#56268](https://github.com/vllm-project/vllm/pull/56268) --tool-strict-level for structural tag activation
- [#53187](https://github.com/vllm-project/vllm/pull/53187) prompt metadata from /inference/v1/generate
- [#43310](https://github.com/vllm-project/vllm/pull/43310) per-request spec decode metrics in generate API
- [#55084](https://github.com/vllm-project/vllm/pull/55084) per-request metrics in Responses API
- [#44890](https://github.com/vllm-project/vllm/pull/44890) release_kv_cache_memory() API
- [#56998](https://github.com/vllm-project/vllm/pull/56998) Rust frontend normalizes native renderer reasoning controls
- [#56777](https://github.com/vllm-project/vllm/pull/56777) Rust frontend returns sampling masks over gRPC
- [#56931](https://github.com/vllm-project/vllm/pull/56931) Rust frontend --hf-overrides
- [#57116](https://github.com/vllm-project/vllm/pull/57116) Rust frontend exposes local DP size in gRPC Control metadata
- [#57033](https://github.com/vllm-project/vllm/pull/57033) Rust frontend per-request preemption histogram
- [#57272](https://github.com/vllm-project/vllm/pull/57272) upgrade XGrammar to 0.2.7 and Rust structural tags to 0.3.0
- [#57520](https://github.com/vllm-project/vllm/pull/57520) remove assistant_token_mask support
- [#57264](https://github.com/vllm-project/vllm/pull/57264) omit absent fields from generate stream chunks (reverted by [#57302](https://github.com/vllm-project/vllm/pull/57302))
- [#57357](https://github.com/vllm-project/vllm/pull/57357) show only docstring summary lines in --help
- [#56271](https://github.com/vllm-project/vllm/pull/56271) parse missing `string=` in DeepSeek V4
- [#51856](https://github.com/vllm-project/vllm/pull/51856) attach request-level tools to existing system message in DSV4 renderer
- [#56635](https://github.com/vllm-project/vllm/pull/56635) fix parser handling of reasoning end/boundary tokens
- [#57058](https://github.com/vllm-project/vllm/pull/57058) reject stop strings on --tokens-only servers

</details>

<details>
<summary>Bugfixes (21)</summary>

- [#57285](https://github.com/vllm-project/vllm/pull/57285) isolate supplemental FlashInfer BF16 autotuning
- [#48956](https://github.com/vllm-project/vllm/pull/48956) fall back to native sampling when FlashInfer cannot target the GPU
- [#51026](https://github.com/vllm-project/vllm/pull/51026) Rust frontend tolerates NaN-corrupted logprobs
- [#56533](https://github.com/vllm-project/vllm/pull/56533) Rust frontend accepts appended EngineCoreOutput fields
- [#55451](https://github.com/vllm-project/vllm/pull/55451) unreadable prompt_embeds returns 400 instead of 500
- [#57076](https://github.com/vllm-project/vllm/pull/57076) bound prompt after multimodal expansion
- [#54283](https://github.com/vllm-project/vllm/pull/54283) frame the multimodal hash digest input
- [#56576](https://github.com/vllm-project/vllm/pull/56576) tolerate malformed EXIF metadata during hashing
- [#56882](https://github.com/vllm-project/vllm/pull/56882) preserve DeepSeek V4 image block spacing
- [#56988](https://github.com/vllm-project/vllm/pull/56988) clean up MCP tool sessions once before closing
- [#51366](https://github.com/vllm-project/vllm/pull/51366) lazy-import model_hosting_container_standards to prevent log suppression
- [#48115](https://github.com/vllm-project/vllm/pull/48115) escape control characters in xgrammar choice grammar
- [#52370](https://github.com/vllm-project/vllm/pull/52370) let optional Literal flag accept None
- [#56904](https://github.com/vllm-project/vllm/pull/56904) make GPU sync checks safe under torch.compile
- [#57070](https://github.com/vllm-project/vllm/pull/57070) size MFU activation traffic from model dtype
- [#51483](https://github.com/vllm-project/vllm/pull/51483) don't classify stateless first chunk as decode for Kimi-K3
- [#57189](https://github.com/vllm-project/vllm/pull/57189) fix Laguna patch mutating flat RoPE parameters
- [#57289](https://github.com/vllm-project/vllm/pull/57289) make nested-RoPE patch reach automatic validation on AMD
- [#57295](https://github.com/vllm-project/vllm/pull/57295) wrong vLLM version from pip install (proto-v* tag collision)
- [#57417](https://github.com/vllm-project/vllm/pull/57417) DiffusionGemma honors logprob_token_ids on converging step
- [#57283](https://github.com/vllm-project/vllm/pull/57283) fix ruff docstring violations in EC connector files

</details>

<details>
<summary>Refactors (7)</summary>

- [#53610](https://github.com/vllm-project/vllm/pull/53610) further cleanup of _apply_hf_processor_main
- [#57674](https://github.com/vllm-project/vllm/pull/57674) use dynamic MM cache in processor
- [#57576](https://github.com/vllm-project/vllm/pull/57576) type dummy options per modality
- [#57194](https://github.com/vllm-project/vllm/pull/57194) remove unused interface methods
- [#54142](https://github.com/vllm-project/vllm/pull/54142) mypy fixes for N/O models
- [#54320](https://github.com/vllm-project/vllm/pull/54320) mypy fixes for Transformers models
- [#57382](https://github.com/vllm-project/vllm/pull/57382) rename --enable-mamba-fine-grained-prefix-cache

</details>

<details>
<summary>Tests (10)</summary>

- [#57127](https://github.com/vllm-project/vllm/pull/57127) hybrid model prefix cache hit-rate coverage
- [#57467](https://github.com/vllm-project/vllm/pull/57467) compute expected hybrid prefix-cache hit instead of hard-coding
- [#55928](https://github.com/vllm-project/vllm/pull/55928) cover get_unhashed_block_ids_all_groups
- [#57385](https://github.com/vllm-project/vllm/pull/57385) adapt ROCm MoE tests to triton_kernels 3.8 API
- [#57112](https://github.com/vllm-project/vllm/pull/57112) fix ROCm MLA RoPE fused-kernel tests for TheRock image
- [#57450](https://github.com/vllm-project/vllm/pull/57450) query HIP device memory for test GPU teardown waits
- [#52956](https://github.com/vllm-project/vllm/pull/52956) delete deprecated torchao v1-config tests
- [#57371](https://github.com/vllm-project/vllm/pull/57371) deflake pooling shards with GPU teardown fixtures
- [#57364](https://github.com/vllm-project/vllm/pull/57364) deflake MTEB score tests
- [#57362](https://github.com/vllm-project/vllm/pull/57362) reclaim GPU memory between model initialization tests

</details>

<details>
<summary>CI & build (11)</summary>

- [#52136](https://github.com/vllm-project/vllm/pull/52136) add pydocstyle to ruff rules (2002 files)
- [#57212](https://github.com/vllm-project/vllm/pull/57212) ignore ruff D209 and rejoin split docstrings
- [#57141](https://github.com/vllm-project/vllm/pull/57141) split slash-combined docstring parameters
- [#57080](https://github.com/vllm-project/vllm/pull/57080) ROCm Stage H gating and MI355 test reallocation
- [#56351](https://github.com/vllm-project/vllm/pull/56351) opt-in TheRock builds for AMD CI
- [#56162](https://github.com/vllm-project/vllm/pull/56162) deprecate DinD for MI250 test groups
- [#56108](https://github.com/vllm-project/vllm/pull/56108) bump Transformers to 5.17.0
- [#57398](https://github.com/vllm-project/vllm/pull/57398) retire Weight Loading smoke tests
- [#57046](https://github.com/vllm-project/vllm/pull/57046) retire Buf schema publishing
- [#41074](https://github.com/vllm-project/vllm/pull/41074) allow installing empty package from pip
- plus 1 more minor CI update ([#56913](https://github.com/vllm-project/vllm/pull/56913))

</details>

<details>
<summary>Docs & other (9)</summary>

- [#56883](https://github.com/vllm-project/vllm/pull/56883) agent instructions for parser directories
- [#57306](https://github.com/vllm-project/vllm/pull/57306) one-step recipe serving
- [#55912](https://github.com/vllm-project/vllm/pull/55912) show how to get Responses prompt token IDs
- [#57083](https://github.com/vllm-project/vllm/pull/57083) retire stale benchmarks, consolidate RMSNorm
- [#57556](https://github.com/vllm-project/vllm/pull/57556) remove unnecessary Transformers version guards
- [#48599](https://github.com/vllm-project/vllm/pull/48599) move env check function to platform interface
- [#56922](https://github.com/vllm-project/vllm/pull/56922) encoder-only ViT CUDA graph capture (MM V2)
- [#53555](https://github.com/vllm-project/vllm/pull/53555) LoRA modules_to_save for sequence classification
- #57057 plus other minor items in the unlisted tail of merged PRs

</details>

<details>
<summary>Newly opened (in progress, highlights)</summary>

- [#57561](https://github.com/vllm-project/vllm/pull/57561) opt-in traced FP8 checkpoint reload
- [#57294](https://github.com/vllm-project/vllm/pull/57294) Qwen3.8-Flash-Next CPU backend
- [#57496](https://github.com/vllm-project/vllm/pull/57496) CPU KDA backend for GLM5Next
- [#57687](https://github.com/vllm-project/vllm/pull/57687) CPU sparse MLA/KeyPool backend for GLM5Next
- [#57129](https://github.com/vllm-project/vllm/pull/57129) fuse_score_remap fused decode score+topk backend for DSA
- [#57682](https://github.com/vllm-project/vllm/pull/57682) CUDA fused QK-norm + RoPE + KV-cache write on FlashAttention
- [#57645](https://github.com/vllm-project/vllm/pull/57645) fuse post-norm, residual add and pre-norm into one op
- [#57428](https://github.com/vllm-project/vllm/pull/57428) fuse MXFP8 wo_b GEMM with sequence-parallel reduce-scatter
- [#57643](https://github.com/vllm-project/vllm/pull/57643) fuse TP all-reduce with mHC input preparation
- [#57673](https://github.com/vllm-project/vllm/pull/57673) native-head Triton sparse MLA for SM90 few-head prefill
- [#57489](https://github.com/vllm-project/vllm/pull/57489) gfx950 FP4 compressed-KV paged attention for DSv4.1
- [#57463](https://github.com/vllm-project/vllm/pull/57463) NVFP4 compressed KV cache on gfx950
- [#57767](https://github.com/vllm-project/vllm/pull/57767) native HIP RDNA3/RDNA4 custom all-reduce
- [#57412](https://github.com/vllm-project/vllm/pull/57412) Kimi-K3 moonmath kernels for gfx942
- [#57709](https://github.com/vllm-project/vllm/pull/57709) FlashInfer experimental FA2 paged-prefill integration
- [#57384](https://github.com/vllm-project/vllm/pull/57384) BerryLM model
- [#57431](https://github.com/vllm-project/vllm/pull/57431) DCP for Qwen4Exp QSA
- [#57239](https://github.com/vllm-project/vllm/pull/57239) DeepSeek-V4 DCP on ROCm (WIP)
- [#57549](https://github.com/vllm-project/vllm/pull/57549) EPLB for dspark draft models
- [#57797](https://github.com/vllm-project/vllm/pull/57797) through [#57805](https://github.com/vllm-project/vllm/pull/57805) attention sinks loaded through weight_loader (RL bugfixes)
- [#57752](https://github.com/vllm-project/vllm/pull/57752) move MediaIO decode into MM preprocessing (experiment, don't merge)
- [#57825](https://github.com/vllm-project/vllm/pull/57825) harden media URL fetching against SSRF

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: d7d55f7d6f3ce9e6d1fd30540c86dfcdcb33dce1e216d79371cc11c23e218d04 -->
