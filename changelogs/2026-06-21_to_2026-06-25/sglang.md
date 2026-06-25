# sglang: PR digest (2026-06-21 to 2026-06-25)

_224 merged, 245 newly opened - source sgl-project/sglang, generated 2026-06-25T11:59:07Z_

## TL;DR
- **DeepSeek-V4** received massive attention, including FP8 MegaMoE support, unified-KV HiSparse on ROCm, and online C128 MTP for EAGLE speculative decoding.
- **MiniMax-M3** saw foundational work with sparse attention ops, JIT kernels, and Wint4Abf16/Win4Afp8 quantization support on Hopper.
- **Performance and kernel optimizations** focused on speculative decoding (DFlash, EAGLE), MoE (NVFP4, FP8), and attention backends (FlashInfer Cascade Attention, Triton sparse-MLA).
- **Significant architectural improvements** include a migration to Mintlify for documentation, a Rust-based Unified Radix Cache (L1 only), and native gRPC server bridging.
- **Hardware support expanded** with Ascend NPU deployment tutorials, Intel XPU graph support, and AMD ROCm optimizations for GLM-5.1 and DeepSeek-V3.2/V4.

## Most important PRs
- **[#28712](https://github.com/sgl-project/sglang/pull/28712) introduces foundational support for MiniMax-M3**
  This merged PR adds sparse attention operations, JIT-compiled kernels, and configuration foundations for both AMD and NVIDIA hardware, paving the way for full MiniMax-M3 integration.
- **[#28964](https://github.com/sgl-project/sglang/pull/28964) migrates the documentation system to Mintlify**
  This newly opened PR replaces the legacy Sphinx documentation system, touching over 250 files to modernize and streamline the project's documentation infrastructure.
- **[#29107](https://github.com/sgl-project/sglang/pull/29107) implements Wint4Abf16 and Win4Afp8 quantization for MiniMax-M3**
  This newly opened PR adds Cutlass and Triton backend support for MiniMax-M3 quantization on NVIDIA Hopper architectures, significantly reducing memory footprint.
- **[#29074](https://github.com/sgl-project/sglang/pull/29074) introduces a Rust-based Unified Radix Cache**
  This newly opened PR implements an L1-only Rust version of the Unified Radix Cache for the scheduler, aiming to improve caching performance and memory safety.
- **[#29048](https://github.com/sgl-project/sglang/pull/29048) adds online w8a8_int8 quantization support for Ascend NPUs**
  This newly opened PR brings Triton kernels and MoE integration for w8a8_int8 quantization to Ascend NPUs, expanding hardware-accelerated quantization capabilities.

## More changes by area

<details>
<summary>Performance (20)</summary>

- [#29117](https://github.com/sgl-project/sglang/pull/29117) optimize CPU GDN prefill performance
- [#28940](https://github.com/sgl-project/sglang/pull/28940) optimize Qwen3-VL / Moss-VL ViT preprocessing
- [#29075](https://github.com/sgl-project/sglang/pull/29075) overlap result D2H copy with the next forward step
- [#28938](https://github.com/sgl-project/sglang/pull/28938) improve performance of DeepSeek-V4 in high concurrency on AMD
- [#22744](https://github.com/sgl-project/sglang/pull/22744) support TF32 matmul to improve MiniMax gate gemm performance on NVIDIA
- [#29105](https://github.com/sgl-project/sglang/pull/29105) precompute mamba conv-state track indices once per batch on NPU
- [#29077](https://github.com/sgl-project/sglang/pull/29077) simplify `_apply_cuda_graph_metadata` for draft extend in trtllm_mla backend
- [#29223](https://github.com/sgl-project/sglang/pull/29223) shard Kimi-K2.5 Eagle3 draft fc + symm-mem AG
- [#29164](https://github.com/sgl-project/sglang/pull/29164) route slow tokenizers through `.encode()` on the `--enable-dynamic-batch-tokenizer` path
- [#28993](https://github.com/sgl-project/sglang/pull/28993) optimize MLA KV buffer gather
- [#28944](https://github.com/sgl-project/sglang/pull/28944) fuse FP8 quantization with DSV4 scale layout write
- [#28983](https://github.com/sgl-project/sglang/pull/28983) enable `SGLANG_OPT_FP8_WO_A_GEMM` on sm90 (Hopper) for DeepSeek-V4
- [#29090](https://github.com/sgl-project/sglang/pull/29090) optimize mla_kv_pack_quantize_fp8 flat kernel and dispatch
- [#29050](https://github.com/sgl-project/sglang/pull/29050) enable dense-MHA prefill on gfx950 (MI350/MI355) for DSA models (GLM-5.1 / DeepSeek-V3.2)
- [#29103](https://github.com/sgl-project/sglang/pull/29103) add DeepSeek-V4 aiter reduce scatter decode
- [#28892](https://github.com/sgl-project/sglang/pull/28892) use unflattened DeepGEMM next-n layout on SM100
- [#29175](https://github.com/sgl-project/sglang/pull/29175) add AITER varlen support to the varlen path
- [#29070](https://github.com/sgl-project/sglang/pull/29070) enable alt stream during BCG prefill
- [#29147](https://github.com/sgl-project/sglang/pull/29147) shard Qwen Text Embed in SP
- [#29202](https://github.com/sgl-project/sglang/pull/29202) enable draft-extend CUDA graph and reduce bubble for MTP
</details>

<details>
<summary>Kernels & attention (32)</summary>

- [#27053](https://github.com/sgl-project/sglang/pull/27053) BCG support and prefill enhancements for GLM5
- [#28670](https://github.com/sgl-project/sglang/pull/28670) add kpool_topk_transform JIT kernel
- [#28450](https://github.com/sgl-project/sglang/pull/28450) fuse shared-expert append + DeepEP remap into one Triton kernel on AMD
- [#28854](https://github.com/sgl-project/sglang/pull/28854) add sync-free `fast_prefill_plan` for EAGLE draft-extend CUDA graph
- [#28084](https://github.com/sgl-project/sglang/pull/28084) fuse topk padded-token masking into a single Triton kernel on AMD
- [#28320](https://github.com/sgl-project/sglang/pull/28320) fused QK GemmaRMSNorm + RoPE + gate kernel for Qwen3.5
- [#29228](https://github.com/sgl-project/sglang/pull/29228) merge dflash triton kernels into a single `dflash.py`
- [#28975](https://github.com/sgl-project/sglang/pull/28975) add opt-in Triton fp8 sparse-MLA prefill kernel for gfx950
- [#27833](https://github.com/sgl-project/sglang/pull/27833) enable BCG on ROCm + route aiter prefill via MHA during PCG/BCG capture for Kimi-2.5
- [#28789](https://github.com/sgl-project/sglang/pull/28789) re-enable SM90 FlashInfer allreduce fusion with safe backend defaults
- [#29019](https://github.com/sgl-project/sglang/pull/29019) cherry-pick re-enable SM90 FlashInfer allreduce fusion
- [#28757](https://github.com/sgl-project/sglang/pull/28757) skip redundant -inf pre-fill of HIP indexer MQA-logits for GLM5
- [#26724](https://github.com/sgl-project/sglang/pull/26724) adaptation to support operator FA3 in deterministic inference on NPU
- [#28782](https://github.com/sgl-project/sglang/pull/28782) support FlashInfer CUDA graph for EAGLE draft-extend
- [#27870](https://github.com/sgl-project/sglang/pull/27870) add XPU support for set_embed_and_head and fused QK RMSNorm kernel for Qwen3.5
- [#28856](https://github.com/sgl-project/sglang/pull/28856) enable FR-Spec in EAGLE draft-extend CUDA graph by sizing logits buffer from the draft head
- [#29047](https://github.com/sgl-project/sglang/pull/29047) add comp-comm overlap kernel generation and integration skills
- [#29304](https://github.com/sgl-project/sglang/pull/29304) NVFP4 KV cache: SM120 + SM121, Gemma-4 VO-split, FP4 prefix-cache correctness
- [#29297](https://github.com/sgl-project/sglang/pull/29297) training-free sparse attention indexer for decode for GLM4-MoE
- [#29288](https://github.com/sgl-project/sglang/pull/29288) add FlashInfer's Cascade Attention Backend for cross-request shared-prefix decode
- [#29168](https://github.com/sgl-project/sglang/pull/29168) enable unified-KV HiSparse on ROCm for DeepSeek-V4
- [#29132](https://github.com/sgl-project/sglang/pull/29132) add `[v,k]` state layout option via `linear_backend="seg_la_vk"`
- [#28880](https://github.com/sgl-project/sglang/pull/28880) add fused topk for MiMo
- [#29281](https://github.com/sgl-project/sglang/pull/29281) add diffusion causal Conv3D cat-pad CUDA fast path for Cosmos3
- [#28939](https://github.com/sgl-project/sglang/pull/28939) optimize fused mamba state scatter kernel
- [#28882](https://github.com/sgl-project/sglang/pull/28882) wire Quest sparse attention into the FlashAttention decode path
- [#29257](https://github.com/sgl-project/sglang/pull/29257) migrate MXFP8 Group GEMM & Quant into JIT
- [#28956](https://github.com/sgl-project/sglang/pull/28956) pack aux hidden states into a preallocated buffer
- [#29142](https://github.com/sgl-project/sglang/pull/29142) run routed experts on main stream in dual-stream MoE
- [#29267](https://github.com/sgl-project/sglang/pull/29267) add indices in chunk_gated_delta_rule for CPU
- [#29027](https://github.com/sgl-project/sglang/pull/29027) add a fast layernorm for diffusion models on NPU
- [#29131](https://github.com/sgl-project/sglang/pull/29131) adapt MiMo-V2.5 kernels
</details>

<details>
<summary>MoE & quantization (24)</summary>

- [#28953](https://github.com/sgl-project/sglang/pull/28953) LoRA BF16 support + EP cuda-graph crash fix for experimental_sgl_trtllm MoE-LoRA
- [#25820](https://github.com/sgl-project/sglang/pull/25820) support NVFP4 MoE for DeepSeek-V4 on NVIDIA
- [#25665](https://github.com/sgl-project/sglang/pull/25665) add GB10 FP8 fused MoE Triton config
- [#29080](https://github.com/sgl-project/sglang/pull/29080) cherry-pick add GB10 FP8 fused MoE Triton config
- [#28689](https://github.com/sgl-project/sglang/pull/28689) dedup triton_kernels backend quant-arg asserts and fill weight dtype guard
- [#27939](https://github.com/sgl-project/sglang/pull/27939) support online MXFP8 quantization for ungated MoE
- [#28942](https://github.com/sgl-project/sglang/pull/28942) gate DeepEP MNNVL on fabric support
- [#28786](https://github.com/sgl-project/sglang/pull/28786) enable FlashInfer allreduce for Qwen3-VL MoE on B300
- [#28974](https://github.com/sgl-project/sglang/pull/28974) refactor weight checker: add precision branch, allow ULP quant err, use chunked compare
- [#29190](https://github.com/sgl-project/sglang/pull/29190) add MoE NVFP4 kernel of B12X for SM120
- [#28985](https://github.com/sgl-project/sglang/pull/28985) auto-tune `num_max_dispatch_tokens_per_rank` from free memory for DeepEP
- [#29112](https://github.com/sgl-project/sglang/pull/29112) support mixed precision models produced by modelopt (mxfp8 linears + nvfp4 experts)
- [#29213](https://github.com/sgl-project/sglang/pull/29213) add checkpoint namespace resolver for fused weights and quant metadata
- [#28928](https://github.com/sgl-project/sglang/pull/28928) add Qwen-Image ModelOpt NVFP4 support
- [#29016](https://github.com/sgl-project/sglang/pull/29016) add SM90 FP8 MegaMoE support for DeepSeek-V4
- [#28932](https://github.com/sgl-project/sglang/pull/28932) fuse down-proj activation quant with silu+mul on AMD
- [#28963](https://github.com/sgl-project/sglang/pull/28963) make ROCm aiter fp8 weight pre-shuffle idempotent for RL weight reload
- [#28957](https://github.com/sgl-project/sglang/pull/28957) quantize DFlash draft outside QKV
- [#28949](https://github.com/sgl-project/sglang/pull/28949) support tie_word_embeddings in Qwen3 MoE
- [#29081](https://github.com/sgl-project/sglang/pull/29081) cache dequantized absorbed MLA weights (w_kc/w_vc) to skip per-step dequant
- [#29113](https://github.com/sgl-project/sglang/pull/29113) opt-in fp8 quant of absorbed MLA weights for fused a8w8 decode (ROCm)
- [#28954](https://github.com/sgl-project/sglang/pull/28954) add dpa for dsr1 fp4
- [#29209](https://github.com/sgl-project/sglang/pull/29209) fuse MLA FP8 latent-cache write via aiter concat_and_cache_mla
- [#28898](https://github.com/sgl-project/sglang/pull/28898) MM test pr28889
</details>

<details>
<summary>Model support (17)</summary>

- [#29052](https://github.com/sgl-project/sglang/pull/29052) add Krea 2 support
- [#28952](https://github.com/sgl-project/sglang/pull/28952) add DeepSeek V4 Flash demo notebook
- [#26574](https://github.com/sgl-project/sglang/pull/26574) add Mooncake group semantics
- [#27392](https://github.com/sgl-project/sglang/pull/27392) add B200 diffusion norm-scale-shift CUDA fast path for Qwen-Image
- [#29051](https://github.com/sgl-project/sglang/pull/29051) add Krea-2 cookbook
- [#28266](https://github.com/sgl-project/sglang/pull/28266) enable cache-dit for ERNIE-Image model
- [#28686](https://github.com/sgl-project/sglang/pull/28686) enable prefill piecewise CUDA graph for Cohere2Vision (text path)
- [#29194](https://github.com/sgl-project/sglang/pull/29194) support GLM-5.1 MXFP4 (MI355X) + enable EAGLE for gfx950
- [#28675](https://github.com/sgl-project/sglang/pull/28675) add mamba-backend and SSM dtype flags for Nemotron3-Ultra
- [#29011](https://github.com/sgl-project/sglang/pull/29011) enable Helios on NPU
- [#29253](https://github.com/sgl-project/sglang/pull/29253) add MiMo V2.5 Blackwell vision FA4 recipe
- [#29186](https://github.com/sgl-project/sglang/pull/29186) add Baidu Unlimited-OCR support
- [#29189](https://github.com/sgl-project/sglang/pull/29189) add Gigachat 3.5 support
- [#28980](https://github.com/sgl-project/sglang/pull/28980) support DeepSeek V4 Flash MTP on Ascend
- [#28958](https://github.com/sgl-project/sglang/pull/28958) support nvidia/LocateAnything-3B
- [#29192](https://github.com/sgl-project/sglang/pull/29192) enable GLM on Xeon
- [#28926](https://github.com/sgl-project/sglang/pull/28926) enable RL rollout path for LTX-2.3 post-training
</details>

<details>
<summary>Parallelism & scheduling (31)</summary>

- [#25090](https://github.com/sgl-project/sglang/pull/25090) support triton backend decode context parallel for Qwen3.5 on AMD
- [#27634](https://github.com/sgl-project/sglang/pull/27634) decoupled speculative decoding: IPC protocol + cross-process request id + server flags
- [#28258](https://github.com/sgl-project/sglang/pull/28258) add NIXL FILE cache cleaner for HiCache
- [#28755](https://github.com/sgl-project/sglang/pull/28755) cap SWA pool sizing with chunk cache
- [#27058](https://github.com/sgl-project/sglang/pull/27058) add session radix cache
- [#22659](https://github.com/sgl-project/sglang/pull/22659) add sleep/wake support for diffusion engine
- [#26245](https://github.com/sgl-project/sglang/pull/26245) support DP-aware PD router dispatch
- [#29089](https://github.com/sgl-project/sglang/pull/29089) extract DFlash prefill refill into a standalone MinFreeSlotsDelayer
- [#27731](https://github.com/sgl-project/sglang/pull/27731) add KV-page double-free checks to the invariant checker
- [#29124](https://github.com/sgl-project/sglang/pull/29124) unify the overlap stash relay behind a RelayPayload dataclass
- [#29225](https://github.com/sgl-project/sglang/pull/29225) unify spec/non-spec decode result handling and overlap relay-payload gating
- [#28779](https://github.com/sgl-project/sglang/pull/28779) add graceful scheduler shutdown; free hisparse host buffer on exit
- [#29118](https://github.com/sgl-project/sglang/pull/29118) fold DFlash verified_id into the shared bonus_tokens relay channel
- [#28363](https://github.com/sgl-project/sglang/pull/28363) gate the overlap WAR barrier on forward reads to recover decode throughput
- [#29207](https://github.com/sgl-project/sglang/pull/29207) add scheduler metrics extension hooks
- [#29187](https://github.com/sgl-project/sglang/pull/29187) add DeepSeek V4 CP KV LayerSplit
- [#29173](https://github.com/sgl-project/sglang/pull/29173) add Reference-aware Radix Cache for agentic multi-turn workloads
- [#28921](https://github.com/sgl-project/sglang/pull/28921) support DSV4 HiSparse online C128 MTP with EAGLE
- [#28998](https://github.com/sgl-project/sglang/pull/28998) add Domino projector support to DFlash speculative decoding (V2)
- [#29049](https://github.com/sgl-project/sglang/pull/29049) HiCache L1-L2-Boundary write policy
- [#28891](https://github.com/sgl-project/sglang/pull/28891) LRU-based Session-level Eviction Policy for StreamingSession
- [#29191](https://github.com/sgl-project/sglang/pull/29191) nixl hicache backend support hybrid models
- [#29193](https://github.com/sgl-project/sglang/pull/29193) make cur_batch/last_batch event-loop locals instead of Scheduler fields
- [#28994](https://github.com/sgl-project/sglang/pull/28994) DeepEP-safe reland of DP mem_fraction_static + DeepEP capacity auto-tuning
- [#29199](https://github.com/sgl-project/sglang/pull/29199) add experimental agent-aware KV cache hints
- [#29033](https://github.com/sgl-project/sglang/pull/29033) support session radix cache in HiCache
- [#29185](https://github.com/sgl-project/sglang/pull/29185) support decode context parallel for DeepSeek V4 with unified kv attention backend
- [#29031](https://github.com/sgl-project/sglang/pull/29031) enable online C128 MTP for EAGLE on DeepSeek-V4
- [#29232](https://github.com/sgl-project/sglang/pull/29232) replace shared-infra dflash special-cases with capabilities (WAR barrier + seq_lens_cpu)
- [#28878](https://github.com/sgl-project/sglang/pull/28878) add cache hit ratio scheduler policy
- [#29218](https://github.com/sgl-project/sglang/pull/29218) DFlash: support cuteDSL/trtllm_mla verify on pure-MLA fp8 targets
</details>

<details>
<summary>Hardware & arch (8)</summary>

- [#27893](https://github.com/sgl-project/sglang/pull/27893) create deployment tutorials for mainstream models on Ascend NPU
- [#28621](https://github.com/sgl-project/sglang/pull/28621) update best practice docs from testcase for NPU
- [#28981](https://github.com/sgl-project/sglang/pull/28981) update v4 cookbook to clean env vars for AMD
- [#28909](https://github.com/sgl-project/sglang/pull/28909) update contribution guide of Ascend NPU
- [#28643](https://github.com/sgl-project/sglang/pull/28643) update features on Ascend NPU
- [#29053](https://github.com/sgl-project/sglang/pull/29053) enable XPU graph support (decode full-graph + prefill tc_piecewise)
- [#28865](https://github.com/sgl-project/sglang/pull/28865) support chunked prefill for DeepSeek-V4 on NPU
- [#28842](https://github.com/sgl-project/sglang/pull/28842) support TBO prefill-only mode on single machine
</details>

<details>
<summary>API & serving (18)</summary>

- [#28674](https://github.com/sgl-project/sglang/pull/28674) sync server arguments and environment variables + update various documentation
- [#23507](https://github.com/sgl-project/sglang/pull/23507) native server: Python bridge entrypoint (2/4)
- [#29104](https://github.com/sgl-project/sglang/pull/29104) add opt-in request-count admission control / backpressure
- [#29242](https://github.com/sgl-project/sglang/pull/29242) Responses API: accept tool_choice object form + streaming disconnect/error parity
- [#29165](https://github.com/sgl-project/sglang/pull/29165) add in-flight request cap (`max_inflight_requests`)
- [#29116](https://github.com/sgl-project/sglang/pull/29116) forward over cleartext h2c to engines that enable HTTP/2
- [#28933](https://github.com/sgl-project/sglang/pull/28933) weight worker selection by priority/cost labels
- [#29251](https://github.com/sgl-project/sglang/pull/29251) record `sgl_router_ttft_seconds` on first content token only
- [#28936](https://github.com/sgl-project/sglang/pull/28936) responses api supports formatted output and modification
- [#29206](https://github.com/sgl-project/sglang/pull/29206) add `--forward-headers` flag to forward custom request headers to upstream workers
- [#29169](https://github.com/sgl-project/sglang/pull/29169) strip `x-anthropic-billing-header` from Anthropic API system prompt
- [#28955](https://github.com/sgl-project/sglang/pull/28955) skip mid-conv system hoist on inline-capable templates
- [#28914](https://github.com/sgl-project/sglang/pull/28914) clamp decode capture bs to DeepEP low_latency buffer
- [#29114](https://github.com/sgl-project/sglang/pull/29114) strip unset tool-schema defaults before apply_chat_template
- [#28943](https://github.com/sgl-project/sglang/pull/28943) DFLASH: support grammar-constrained decoding (JSON schema / regex / ebnf / structural_tag)
- [#28822](https://github.com/sgl-project/sglang/pull/28822) add `system_fingerprint` to Python OpenAI chat/completion responses
- [#29017](https://github.com/sgl-project/sglang/pull/29017) PD router: cancel paired decode when prefill fails
- [#29167](https://github.com/sgl-project/sglang/pull/29167) add index cache config from model's config.json
</details>

<details>
<summary>Refactors (17)</summary>

- [#28919](https://github.com/sgl-project/sglang/pull/28919) migrate all ServerArgs fields to Annotated style, reduce add_cli_args by ~2400 lines
- [#28001](https://github.com/sgl-project/sglang/pull/28001) refactor weight processing in RL weight update
- [#28492](https://github.com/sgl-project/sglang/pull/28492) refactor / simplify `MultiLayerEagleDraftExtendCudaGraphRunner` to use rotation
- [#28830](https://github.com/sgl-project/sglang/pull/28830) migrate more server args to annotated style
- [#28814](https://github.com/sgl-project/sglang/pull/28814) auto-derive CLI args from dataclass fields to eliminate duplication
- [#29214](https://github.com/sgl-project/sglang/pull/29214) IPC struct renames, better typing, and SenderWrapper removal
- [#29012](https://github.com/sgl-project/sglang/pull/29012) introduce sock_send/sock_recv wrappers for zmq IPC
- [#28888](https://github.com/sgl-project/sglang/pull/28888) refactor causal KV local head cache updates
- [#28833](https://github.com/sgl-project/sglang/pull/28833) bound DiffGenerator local cleanup
- [#28973](https://github.com/sgl-project/sglang/pull/28973) share CUDA graph memory pool across prefill and decode
- [#28968](https://github.com/sgl-project/sglang/pull/28968) remove dead out_cache_loc_swa buffers
- [#28978](https://github.com/sgl-project/sglang/pull/28978) enhance mechanical refactor skills and large class styles and code styles
- [#29224](https://github.com/sgl-project/sglang/pull/29224) style and type annotation improvements extracted from #28688
- [#29285](https://github.com/sgl-project/sglang/pull/29285) unify draft runner accessor naming and remove dispatch band-aids
- [#28970](https://github.com/sgl-project/sglang/pull/28970) decouple TRTLLMHAAttnBackend from FlashInferAttnBackend
- [#28962](https://github.com/sgl-project/sglang/pull/28962) move checkpoint-completeness check into the loader
- [#28820](https://github.com/sgl-project/sglang/pull/28820) decouple TRTLLM MHA backends from FlashInfer inheritance
</details>

<details>
<summary>Bugfixes (120)</summary>

- [#25071](https://github.com/sgl-project/sglang/pull/25071) fix kimik2_detector normal text detection before tool call
- [#28601](https://github.com/sgl-project/sglang/pull/28601) return streaming logprobs when reasoning/tool parser is active
- [#26880](https://github.com/sgl-project/sglang/pull/26880) fix EAGLE draft graph seq_lens_sum padding
- [#26773](https://github.com/sgl-project/sglang/pull/26773) handle mid-conversation system messages for Anthropic
- [#28237](https://github.com/sgl-project/sglang/pull/28237) correct fused shared-expert scaling on aiter/DeepEP path (mori all-to-all)
- [#28832](https://github.com/sgl-project/sglang/pull/28832) fix Qwen-Image-Layered latent shape
- [#28870](https://github.com/sgl-project/sglang/pull/28870) restore EAGLE prefill plumbing dropped by #23906
- [#28770](https://github.com/sgl-project/sglang/pull/28770) fix Apple Silicon server startup; align MLX tests with upstream
- [#28988](https://github.com/sgl-project/sglang/pull/28988) fix lint brought by [#27527](https://github.com/sgl-project/sglang/pull/27527)
- [#28990](https://github.com/sgl-project/sglang/pull/28990) fix main's lint
- [#28781](https://github.com/sgl-project/sglang/pull/28781) restore Hunyuan3D-2 image-to-3D
- [#29069](https://github.com/sgl-project/sglang/pull/29069) autotune flashinfer MoE on a decode-shaped buffer
- [#29086](https://github.com/sgl-project/sglang/pull/29086) cherry-pick autotune flashinfer MoE on a decode-shaped buffer
- [#28916](https://github.com/sgl-project/sglang/pull/28916) fix hicache host memory leak by bounding PP-sync work_list
- [#27430](https://github.com/sgl-project/sglang/pull/27430) use full conversation for PD chat cache-aware routing
- [#28769](https://github.com/sgl-project/sglang/pull/28769) fix SANA VAE dtype and TurboWan backend selection
- [#28337](https://github.com/sgl-project/sglang/pull/28337) place TBO cuda-graph num_token_non_padded buffer on model devices
- [#28144](https://github.com/sgl-project/sglang/pull/28144) fix TRTLLM MHA FP8 KV cache scale handling
- [#29245](https://github.com/sgl-project/sglang/pull/29245) cherry-pick fix TRTLLM MHA FP8 KV cache scale handling
- [#26980](https://github.com/sgl-project/sglang/pull/26980) skip routed expert capture for draft model under spec v2
- plus 100 more minor bugfixes
</details>

<details>
<summary>Tests, CI & build (130)</summary>

- [#28082](https://github.com/sgl-project/sglang/pull/28082) refactor weight checker ULP-based quant error tolerance
- [#27527](https://github.com/sgl-project/sglang/pull/27527) vectorize `_create_custom_4d_mask` in CustomQwen2Decoder
- [#28449](https://github.com/sgl-project/sglang/pull/28449) expand parser auto detection coverage
- [#29098](https://github.com/sgl-project/sglang/pull/29098) extract profile request cleanups
- [#28855](https://github.com/sgl-project/sglang/pull/28855) split init_backends; account draft weights in `--mem-fraction-static`
- [#29220](https://github.com/sgl-project/sglang/pull/29220) dissolve `EagleDraftInputV2Mixin` so spec-info dataclasses hold data only
- [#28683](https://github.com/sgl-project/sglang/pull/28683) split init_backends; account draft weights in `--mem-fraction-static`
- [#28841](https://github.com/sgl-project/sglang/pull/28841) revert split init_backends
- [#29198](https://github.com/sgl-project/sglang/pull/29198) convert SamplingParams to msgspec Struct
- [#28813](https://github.com/sgl-project/sglang/pull/28813) refactor int checkpoint tests style
- plus 120 more minor test and CI updates
</details>

<details>
<summary>Docs & Other (47)</summary>

- [#28522](https://github.com/sgl-project/sglang/pull/28522) add Anthropic-compatible API documentation
- [#29051](https://github.com/sgl-project/sglang/pull/29051) add Krea-2 cookbook
- [#29129](https://github.com/sgl-project/sglang/pull/29129) fix TOC of Ascend NPU Docs
- [#28774](https://github.com/sgl-project/sglang/pull/28774) Laguna-M.1 playground: add HiCache; refresh EP / DP-Attention notes
- [#28816](https://github.com/sgl-project/sglang/pull/28816) add project rule: prefer msgspec.Struct over dataclasses
- [#29226](https://github.com/sgl-project/sglang/pull/29226) add Command A+ cookbook
- [#29276](https://github.com/sgl-project/sglang/pull/29276) add mimo-v2-flash best practice
- [#29293](https://github.com/sgl-project/sglang/pull/29293) add environment prerequisites to model tutorials
- [#29302](https://github.com/sgl-project/sglang/pull/29302) fix diffusion docs and cookbook drift
- [#28937](https://github.com/sgl-project/sglang/pull/28937) clean up CUDA graph capture logs
- plus 37 more minor documentation and miscellaneous updates
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
