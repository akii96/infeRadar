# vllm: PR digest (2026-09-13 to 2026-09-17)

_297 merged, 424 newly opened - source vllm-project/vllm, generated 2026-09-17T14:25:51Z_

## TL;DR
- **DeepSeek V4/V4.1 dominated this window** (67 labeled PRs). Merged work covered the FlashMLA mega attention path, NVFP4 and MXFP8 compressed KV caches, the Mega-mHC kernel from DeepGEMM, MegaMoE padding removal, and Engram async prefetch. Opened PRs add skinny-GEMM dispatch, decode context parallelism, and prefill compaction.
- **Sparse attention and indexer top-k saw the most kernel work.** Merged: DeepGEMM sparse MQA logits, DeepSelect TopK, persistent top-k sampled filtering, and FlashKDA for GLM-5.3-Flash prefill (reported 1.7-3.8x faster than the Triton chunk path). ROCm gfx950 got decode top-k and mHC-fusion tuning for DSV4.1.
- **KV offload and disaggregated serving hardening** was the biggest bugfix cluster: NIXL, Mooncake, HMA/SWA, hybrid-model and MTP paths, plus new P2P, KVCR and CPU-offload features.
- **Housekeeping was heavy:** a repo-wide pydocstyle/ruff change touched about 2000 files, and the Rust frontend and CI sharding both got large PRs. Several Triton JIT-warmup migrations were reverted ([#56654](https://github.com/vllm-project/vllm/pull/56654), [#57132](https://github.com/vllm-project/vllm/pull/57132)).
- Direction: DSV4.1 and GLM-5.3 efficiency across NVIDIA Blackwell and AMD gfx950, speculative decoding (DSpark/DFlash/MTP), and a maturing Rust frontend.

## Most important PRs
**[#56935](https://github.com/vllm-project/vllm/pull/56935) DSv4.1 FlashMLA mega attention and NVFP4 compressed KV cache (merged)**
Adds the FlashMLA mega attention path with an NVFP4 compressed KV cache for DeepSeek V4.1, cutting KV memory. [#56893](https://github.com/vllm-project/vllm/pull/56893) follows with an MXFP8 whole-KV record.

**[#56254](https://github.com/vllm-project/vllm/pull/56254) DeepGEMM sparse MQA logits in the DSV4.1 indexer (merged)**
Routes the DSA indexer through DeepGEMM's sparse MQA logits kernel, speeding long-context sparse attention. [#56464](https://github.com/vllm-project/vllm/pull/56464) pairs it with a DeepSelect top-k.

**[#56633](https://github.com/vllm-project/vllm/pull/56633) Fold mHC post block into delayed pre projection (merged)**
Fuses the mHC post step into the next layer's pre projection for DSV4.1, removing a pass per layer. [#56513](https://github.com/vllm-project/vllm/pull/56513) does the same on ROCm, and [#56962](https://github.com/vllm-project/vllm/pull/56962) integrates DeepGEMM's Mega-mHC.

**[#56512](https://github.com/vllm-project/vllm/pull/56512) Engram async prefetch and DP sharding (merged)**
Offloaded Engram lookups are prefetched asynchronously and sharded across data-parallel ranks, hiding host-table latency in V4.1.

**[#55737](https://github.com/vllm-project/vllm/pull/55737) FlashKDA for GLM-5.3-Flash KDA chunked prefill (merged)**
Replaces the Triton chunk path with FlashKDA, reported 1.7-3.8x faster prefill.

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#56346](https://github.com/vllm-project/vllm/pull/56346) sampled filtering for persistent top-k
- [#53793](https://github.com/vllm-project/vllm/pull/53793) fuse ReLU2 with static FP8 activation quant
- [#56478](https://github.com/vllm-project/vllm/pull/56478) fix odd-row perf cliff in per-token-group quant
- [#57204](https://github.com/vllm-project/vllm/pull/57204) remove MegaMoE padding workaround for DSV4.1
- [#56568](https://github.com/vllm-project/vllm/pull/56568) pad shared experts for native MegaMoE fusion
- [#54674](https://github.com/vllm-project/vllm/pull/54674) stack DSpark context WKV projections
- [#56441](https://github.com/vllm-project/vllm/pull/56441) KV-only context insertion across V4.1 cache formats
- [#57095](https://github.com/vllm-project/vllm/pull/57095) batch image requests per encoder (EPD)
- [#56657](https://github.com/vllm-project/vllm/pull/56657) reduce EPD proxy serialization overhead
- [#48498](https://github.com/vllm-project/vllm/pull/48498) Triton kernel for Gemma3n sparse GELU
- [#57273](https://github.com/vllm-project/vllm/pull/57273) sm_90 tuning table for Qwen4Exp QSA
- [#55738](https://github.com/vllm-project/vllm/pull/55738) dense/masked-MHA sparse prefill for GLM NoPE layout
- [#51794](https://github.com/vllm-project/vllm/pull/51794) and [#56853](https://github.com/vllm-project/vllm/pull/56853) CSA and HCA multi-stream overlap on ROCm DeepSeek-V4
- [#57229](https://github.com/vllm-project/vllm/pull/57229) reduce CUDA graph divergences on ROCm

</details>

<details>
<summary>Kernels & attention (8)</summary>

- [#56305](https://github.com/vllm-project/vllm/pull/56305) Triton/FlashInfer composite for multimodal prefix attention
- [#55879](https://github.com/vllm-project/vllm/pull/55879) stabilize sparse-MLA DCP for GLM PCP evals
- [#55538](https://github.com/vllm-project/vllm/pull/55538) write nvfp4_ds_mla from fused norm+rope kernel
- [#56825](https://github.com/vllm-project/vllm/pull/56825) fix sparse-MLA piecewise cudagraph capture crash
- [#56715](https://github.com/vllm-project/vllm/pull/56715) respect interleave in PCP/DCP indexer KV gather
- [#51367](https://github.com/vllm-project/vllm/pull/51367) Murmur3 RNG for Gumbel sampling
- [#55991](https://github.com/vllm-project/vllm/pull/55991) skip AITER norm kernels when flattening would copy
- [#56845](https://github.com/vllm-project/vllm/pull/56845) remove dead kernel code (1,895 lines)

</details>

<details>
<summary>MoE & quantization (13)</summary>

- [#54699](https://github.com/vllm-project/vllm/pull/54699) convert FlashInfer BF16 MoE weights in place
- [#55867](https://github.com/vllm-project/vllm/pull/55867) FP8 TP with FlashInfer TRTLLM MoE for Qwen3.8-Flash-Next
- [#52781](https://github.com/vllm-project/vllm/pull/52781) DeepEP v2 async finalize to overlap shared experts with combine
- [#55316](https://github.com/vllm-project/vllm/pull/55316) W8A8 INT8 MoE on POWER
- [#55934](https://github.com/vllm-project/vllm/pull/55934) ROCm triton 3.8 mxfp4 MoE (gpt-oss, DeepSeek-V4)
- [#53940](https://github.com/vllm-project/vllm/pull/53940) a4w4 flydsl kernels for Kimi-K3 on ROCm
- [#56560](https://github.com/vllm-project/vllm/pull/56560) dequantize MXFP8 weight once when dot_scaled is unavailable
- [#54965](https://github.com/vllm-project/vllm/pull/54965) keep W4A16 skinny GEMM zero-points packed
- [#54248](https://github.com/vllm-project/vllm/pull/54248) expose kFp8DynamicTokenSym on AITER PTPC linears
- [#56985](https://github.com/vllm-project/vllm/pull/56985) per-tensor FP8 W8A16 CPU kernel for Ministral
- [#51204](https://github.com/vllm-project/vllm/pull/51204) select linear backends per quantization
- [#53914](https://github.com/vllm-project/vllm/pull/53914) fix DeepGEMM FP8 workspace over-allocation
- [#57074](https://github.com/vllm-project/vllm/pull/57074) AITER FP8 modular-kernel sweep and MoRI dispatch fix

</details>

<details>
<summary>Model support (11)</summary>

- [#55557](https://github.com/vllm-project/vllm/pull/55557) Qwen4Exp fp8_e4m3 KV cache on QSA path
- [#55309](https://github.com/vllm-project/vllm/pull/55309) Qwen3.8-Flash-Next PLE residual and QSA gate fusion
- [#55768](https://github.com/vllm-project/vllm/pull/55768) Gemma 4 de-JITification
- [#51167](https://github.com/vllm-project/vllm/pull/51167) Voxtral Realtime FULL_DECODE_ONLY CUDA graphs
- [#55897](https://github.com/vllm-project/vllm/pull/55897) LoRA for DeepSeek-V4 Flash Vision
- [#56231](https://github.com/vllm-project/vllm/pull/56231) LoRA for Nemotron VL
- [#53555](https://github.com/vllm-project/vllm/pull/53555) LoRA modules_to_save for sequence classification
- [#56176](https://github.com/vllm-project/vllm/pull/56176) GLM-5.3-Flash Quark MXFP4 checkpoint on ROCm
- [#57189](https://github.com/vllm-project/vllm/pull/57189) fix Laguna patch mutating flat RoPE params
- [#56408](https://github.com/vllm-project/vllm/pull/56408) XGrammar schema constraints for DeepSeek V4.1
- [#56741](https://github.com/vllm-project/vllm/pull/56741) normalize DSV4.1 package naming

</details>

<details>
<summary>Parallelism & scheduling (15)</summary>

- [#48200](https://github.com/vllm-project/vllm/pull/48200) StructuredOutputManager x spec decode refactor
- [#52228](https://github.com/vllm-project/vllm/pull/52228) MRV2 acceptance estimation for adaptive verification
- [#51700](https://github.com/vllm-project/vllm/pull/51700) MRV2 FULL CUDA graph for DBO microbatched steps
- [#53867](https://github.com/vllm-project/vllm/pull/53867) PCP decode-only FULL CUDA graphs
- [#56922](https://github.com/vllm-project/vllm/pull/56922) encoder-only ViT CUDA graph capture
- [#56758](https://github.com/vllm-project/vllm/pull/56758) `--max-num-active-seqs` to cap RUNNING admission
- [#44987](https://github.com/vllm-project/vllm/pull/44987) XPU EPLB
- [#56930](https://github.com/vllm-project/vllm/pull/56930) fix EAGLE and dense draft startup with EP
- [#56387](https://github.com/vllm-project/vllm/pull/56387) avoid uninitialized EPLB state in DSpark drafter
- [#55133](https://github.com/vllm-project/vllm/pull/55133) Qwen3 DSpark d2t fix
- [#53458](https://github.com/vllm-project/vllm/pull/53458) draft_id_to_target_id only when vocab differs
- [#55966](https://github.com/vllm-project/vllm/pull/55966) Aiter MLA non-causal draft block decode on ROCm
- [#55055](https://github.com/vllm-project/vllm/pull/55055) fix multi-layer MTP KV during P/D
- [#57104](https://github.com/vllm-project/vllm/pull/57104) fix KVConnector+MTP deadlock under KV pressure
- [#56888](https://github.com/vllm-project/vllm/pull/56888) MRV2 buffer util simplifications

</details>

<details>
<summary>KV cache, offload & connectors (22)</summary>

- [#53624](https://github.com/vllm-project/vllm/pull/53624) KVCR secondary-tier adapter
- [#50494](https://github.com/vllm-project/vllm/pull/50494) NIXL attention-HMA layouts in PP push prefill
- [#56242](https://github.com/vllm-project/vllm/pull/56242) cross-encoder caching for Mooncake P2P
- [#53721](https://github.com/vllm-project/vllm/pull/53721) SWA+HMA in MoRI-IO connector (Gemma4)
- [#55885](https://github.com/vllm-project/vllm/pull/55885) per-request max_load_tokens
- [#54960](https://github.com/vllm-project/vllm/pull/54960) EC connector metrics
- [#53453](https://github.com/vllm-project/vllm/pull/53453) configurable unbound-store timeout for P2P
- [#56645](https://github.com/vllm-project/vllm/pull/56645) expose PCP producer KV shards as NIXL ranks
- [#51787](https://github.com/vllm-project/vllm/pull/51787) track cache recency once per request
- [#56855](https://github.com/vllm-project/vllm/pull/56855) and [#50984](https://github.com/vllm-project/vllm/pull/50984) Mooncake request-level KV load failures
- [#55027](https://github.com/vllm-project/vllm/pull/55027) MooncakeStore excludes non-prefix-cacheable groups
- [#50388](https://github.com/vllm-project/vllm/pull/50388) fix ValueError on KV load failure with hybrid cache
- [#56104](https://github.com/vllm-project/vllm/pull/56104) NIXL multi-handle xfer race
- [#56640](https://github.com/vllm-project/vllm/pull/56640) NIXL full prefix hit reported finished
- [#56317](https://github.com/vllm-project/vllm/pull/56317) NixlPush _remote_agents guard
- [#54014](https://github.com/vllm-project/vllm/pull/54014) and [#51081](https://github.com/vllm-project/vllm/pull/51081) CPU offload cgroup check and chunked registration
- [#55823](https://github.com/vllm-project/vllm/pull/55823), [#56621](https://github.com/vllm-project/vllm/pull/56621), [#56709](https://github.com/vllm-project/vllm/pull/56709), [#56486](https://github.com/vllm-project/vllm/pull/56486), [#56799](https://github.com/vllm-project/vllm/pull/56799), [#57145](https://github.com/vllm-project/vllm/pull/57145) KV offload fixes (lookup probes, no-forward stores, MTP SWA history, sliding windows, MLA rows, scratch groups)
- [#57077](https://github.com/vllm-project/vllm/pull/57077) HiSparse PD region-mapped pulls
- [#57027](https://github.com/vllm-project/vllm/pull/57027) HiSparse per-layer offsets
- [#50894](https://github.com/vllm-project/vllm/pull/50894) KV page size for hidden-states extraction with TP
- [#57050](https://github.com/vllm-project/vllm/pull/57050) Mamba block allocation estimate

</details>

<details>
<summary>API & serving (22)</summary>

- [#56998](https://github.com/vllm-project/vllm/pull/56998) Rust frontend reasoning controls
- [#56567](https://github.com/vllm-project/vllm/pull/56567) Rust frontend HTTP RL weight sync
- [#56931](https://github.com/vllm-project/vllm/pull/56931) Rust frontend `--hf-overrides`
- [#57116](https://github.com/vllm-project/vllm/pull/57116) Rust frontend local DP size in gRPC Control
- [#56990](https://github.com/vllm-project/vllm/pull/56990) Rust frontend iteration token histogram
- [#56338](https://github.com/vllm-project/vllm/pull/56338) Rust frontend per-request watermarking controls
- [#53187](https://github.com/vllm-project/vllm/pull/53187) prompt metadata from /inference/v1/generate
- [#57264](https://github.com/vllm-project/vllm/pull/57264) omit absent fields from generate stream chunks (reverted by [#57302](https://github.com/vllm-project/vllm/pull/57302))
- [#55084](https://github.com/vllm-project/vllm/pull/55084) per-request metrics in Responses API
- [#55176](https://github.com/vllm-project/vllm/pull/55176) `--enable-scale-out` replaces env var
- [#54746](https://github.com/vllm-project/vllm/pull/54746) share max_num_queued_reqs across API servers
- [#56746](https://github.com/vllm-project/vllm/pull/56746) move grpc_server to launchers
- [#42904](https://github.com/vllm-project/vllm/pull/42904) xgrammar patternProperties support
- [#55283](https://github.com/vllm-project/vllm/pull/55283) clarify ITL vs TPOT Prometheus metrics
- [#55624](https://github.com/vllm-project/vllm/pull/55624) SWA and hybrid in MFU/MBU estimation
- [#51084](https://github.com/vllm-project/vllm/pull/51084) Proton CUDA graph attribution for MRV2
- [#55508](https://github.com/vllm-project/vllm/pull/55508) consistent streaming TTFT/E2E accounting in benchmark
- [#55468](https://github.com/vllm-project/vllm/pull/55468) fast loader nnode>1
- [#56669](https://github.com/vllm-project/vllm/pull/56669) GPU uuid as socket folder id
- [#56908](https://github.com/vllm-project/vllm/pull/56908) MRV2 tolerates no pinned memory
- [#56200](https://github.com/vllm-project/vllm/pull/56200) derive is_reasoning_end from engine grammar
- #56133-class parser fixes: [#56635](https://github.com/vllm-project/vllm/pull/56635), [#53444](https://github.com/vllm-project/vllm/pull/53444)

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#56743](https://github.com/vllm-project/vllm/pull/56743) ROCm DSV4.1 K=512 decode top-k on gfx950
- [#56628](https://github.com/vllm-project/vllm/pull/56628) ROCm DSA decode candidate mask striding
- [#55235](https://github.com/vllm-project/vllm/pull/55235) ROCm MiniMax-M3 decode top-k tuning
- [#56015](https://github.com/vllm-project/vllm/pull/56015) XPU device_ids placement
- [#54923](https://github.com/vllm-project/vllm/pull/54923) CPU fallback when zentorch import fails

</details>

<details>
<summary>Bugfixes (20)</summary>

- [#57132](https://github.com/vllm-project/vllm/pull/57132) revert two ROCm changes to fix DeepSeek-V4 accuracy
- [#57152](https://github.com/vllm-project/vllm/pull/57152) restore causal image SWA for DSV4.1
- [#56366](https://github.com/vllm-project/vllm/pull/56366) DSV4.1 and Kimi K3 media placeholders in Rust frontend
- [#56593](https://github.com/vllm-project/vllm/pull/56593) add_generation_prompt in DeepSeek renderers
- [#56706](https://github.com/vllm-project/vllm/pull/56706) stale HPC QK-norm weights after refit
- [#57285](https://github.com/vllm-project/vllm/pull/57285) isolate FlashInfer BF16 autotuning
- [#48956](https://github.com/vllm-project/vllm/pull/48956) native sampling fallback when FlashInfer cannot target GPU
- [#56930](https://github.com/vllm-project/vllm/pull/56930)-adjacent: [#56249](https://github.com/vllm-project/vllm/pull/56249) beam search aborted requests
- [#56211](https://github.com/vllm-project/vllm/pull/56211) beam search skip_special_tokens
- [#56844](https://github.com/vllm-project/vllm/pull/56844) validate routed-expert prompt offsets
- [#55451](https://github.com/vllm-project/vllm/pull/55451) unreadable prompt_embeds returns 400
- [#51483](https://github.com/vllm-project/vllm/pull/51483) and [#56794](https://github.com/vllm-project/vllm/pull/56794) Kimi-K3 fixes
- [#56652](https://github.com/vllm-project/vllm/pull/56652) and [#56721](https://github.com/vllm-project/vllm/pull/56721) Gemma4 fixes
- [#56432](https://github.com/vllm-project/vllm/pull/56432), [#56786](https://github.com/vllm-project/vllm/pull/56786), [#56576](https://github.com/vllm-project/vllm/pull/56576) multimodal and EPD fixes
- [#56726](https://github.com/vllm-project/vllm/pull/56726) and [#56590](https://github.com/vllm-project/vllm/pull/56590) ROCm AITER fallbacks
- [#57192](https://github.com/vllm-project/vllm/pull/57192) deferred tilelang.jit on ROCm
- [#56904](https://github.com/vllm-project/vllm/pull/56904) GPU sync checks under torch.compile
- [#56687](https://github.com/vllm-project/vllm/pull/56687) Ray NIXL agents for sharded RDT
- plus 6 more minor fixes ([#51026](https://github.com/vllm-project/vllm/pull/51026), [#56533](https://github.com/vllm-project/vllm/pull/56533), [#56406](https://github.com/vllm-project/vllm/pull/56406), [#56915](https://github.com/vllm-project/vllm/pull/56915), [#57068](https://github.com/vllm-project/vllm/pull/57068), [#56988](https://github.com/vllm-project/vllm/pull/56988))

</details>

<details>
<summary>Refactors (7)</summary>

- [#53610](https://github.com/vllm-project/vllm/pull/53610) cleanup _apply_hf_processor_main
- [#55358](https://github.com/vllm-project/vllm/pull/55358) move sparse_attn_indexer_kpool, split AMD/NVIDIA
- [#55071](https://github.com/vllm-project/vllm/pull/55071) unify multimodal LoRA token count hooks
- [#56898](https://github.com/vllm-project/vllm/pull/56898) remove tpu_input_batch.py
- [#57194](https://github.com/vllm-project/vllm/pull/57194) remove unused interface methods
- [#52956](https://github.com/vllm-project/vllm/pull/52956) delete deprecated torchao tests
- [#56654](https://github.com/vllm-project/vllm/pull/56654) revert explicit Triton JIT warmup migration

</details>

<details>
<summary>Warmup / JIT (3)</summary>

- [#56323](https://github.com/vllm-project/vllm/pull/56323) migrate sampling and DFlash JIT kernels
- [#50178](https://github.com/vllm-project/vllm/pull/50178) migrate MHC TileLang kernels
- [#57083](https://github.com/vllm-project/vllm/pull/57083) retire stale benchmarks, consolidate RMSNorm

</details>

<details>
<summary>Tests (7)</summary>

- [#57127](https://github.com/vllm-project/vllm/pull/57127) hybrid model prefix-cache hit-rate coverage
- [#56528](https://github.com/vllm-project/vllm/pull/56528) VLM batch invariance determinism
- [#56309](https://github.com/vllm-project/vllm/pull/56309) watermarking e2e and GSM8K tests
- [#54934](https://github.com/vllm-project/vllm/pull/54934) CPU CI speculative decoding coverage
- [#57112](https://github.com/vllm-project/vllm/pull/57112) MLA RoPE fused-kernel tests for TheRock
- [#57357](https://github.com/vllm-project/vllm/pull/57357) `--help` shows only summary line of config docstrings
- [#57226](https://github.com/vllm-project/vllm/pull/57226) no blocking collective RPC during handshake

</details>

<details>
<summary>CI & build (14)</summary>

- [#52136](https://github.com/vllm-project/vllm/pull/52136) add pydocstyle to ruff rules
- [#57212](https://github.com/vllm-project/vllm/pull/57212) ignore ruff D209 and rejoin docstrings
- [#57080](https://github.com/vllm-project/vllm/pull/57080) ROCm Stage H gating and MI355 test reallocation
- [#56108](https://github.com/vllm-project/vllm/pull/56108) bump Transformers to 5.17.0
- [#56169](https://github.com/vllm-project/vllm/pull/56169) check target branch freshness before CI
- [#56747](https://github.com/vllm-project/vllm/pull/56747) GPU memory telemetry for MIG slices
- [#56695](https://github.com/vllm-project/vllm/pull/56695) H200 workloads on 18GB MIG slices
- [#56351](https://github.com/vllm-project/vllm/pull/56351) opt-in TheRock builds for AMD CI
- [#56876](https://github.com/vllm-project/vllm/pull/56876) DeepGEMM pin moved to vLLM fork
- [#56941](https://github.com/vllm-project/vllm/pull/56941) and [#56766](https://github.com/vllm-project/vllm/pull/56766) OTel sampler privilege and bytecode fixes
- [#57046](https://github.com/vllm-project/vllm/pull/57046) retire Buf schema publishing
- [#56704](https://github.com/vllm-project/vllm/pull/56704) XPU test requirements
- [#41074](https://github.com/vllm-project/vllm/pull/41074) allow empty package install from pip
- [#56883](https://github.com/vllm-project/vllm/pull/56883) agent instructions for parser directories

</details>

<details>
<summary>Docs (1)</summary>

- [#55912](https://github.com/vllm-project/vllm/pull/55912) show how to get Responses prompt token IDs

</details>

<details>
<summary>Other (2)</summary>

- [#55656](https://github.com/vllm-project/vllm/pull/55656) clean up fast loader daemon quant verification
- [#57041](https://github.com/vllm-project/vllm/pull/57041) infer HiSparse attention config from HiSparseConnector

</details>

<details>
<summary>Newly opened, in progress (selected highlights)</summary>

- [#57057](https://github.com/vllm-project/vllm/pull/57057) UltraQuant 4-bit KV cache backend (FlyDSL)
- [#57129](https://github.com/vllm-project/vllm/pull/57129) fuse_score_remap fused decode score+topk
- [#56685](https://github.com/vllm-project/vllm/pull/56685) Humming quantization integration
- [#56694](https://github.com/vllm-project/vllm/pull/56694) DSpark W2 matrix top-k pruning
- [#56738](https://github.com/vllm-project/vllm/pull/56738) eager MRV2 decode context parallelism for DSv4.1
- [#56751](https://github.com/vllm-project/vllm/pull/56751) skinny GEMM for tiny-M DSV4.1 decode
- [#57294](https://github.com/vllm-project/vllm/pull/57294) CPU backend for Qwen3.8-Flash-Next
- [#57384](https://github.com/vllm-project/vllm/pull/57384) BerryLM model
- [#57135](https://github.com/vllm-project/vllm/pull/57135) Xing4_0 model
- [#56963](https://github.com/vllm-project/vllm/pull/56963) Responses session store
- [#57325](https://github.com/vllm-project/vllm/pull/57325) joint GPU/CPU prefix cache lookup
- [#57073](https://github.com/vllm-project/vllm/pull/57073) FlashInfer CFT MoE all-to-all
- [#56686](https://github.com/vllm-project/vllm/pull/56686) DSV4.1-Flash attention sparse candidate-block work (offline throughput 24.60 s to 22.84 s per 1000 requests on 8 x B200)
- [#56956](https://github.com/vllm-project/vllm/pull/56956) and [#56957](https://github.com/vllm-project/vllm/pull/56957) DSpark PP support
- [#57021](https://github.com/vllm-project/vllm/pull/57021) experimental MXFP8 wo_b GEMM fused with sequence-parallel reduce-scatter (marked do-not-merge)
- plus roughly 400 more opened PRs, mostly DSV4.1/GLM-5.3 perf, KV offload, Rust frontend, watermarking and CI sharding

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 786882c34b88746ca2915b6780e3fbf9f3b4d861bbd2cafa0fb427b5e5b7495a -->
