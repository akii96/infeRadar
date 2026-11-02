# sglang: PR digest (2026-10-29 to 2026-11-02)

_316 merged, 424 newly opened - source sgl-project/sglang, generated 2026-11-02T00:52:43Z_

## TL;DR
- **DeepSeek (V4/V4.1) and MiniMax (M3/M3.1/H3) got the most attention.** Merged work is mostly AMD gfx950 kernels for MiniMax, plus DSv4.1 indexer, wo_a GEMM and draft-logit work. Open PRs add SM90/SM100/SM120 DSv4.1 kernels, NPU A5 and CPU ports, and CP/DP-attention support.
- **Performance work centers on speculative decoding and fused kernels.** Merged: DSpark and DFlash fixes, a sharded-accept path that drops the whole-vocab draft-logit gather, Qwen3 fused QK-norm+RoPE for decode, and MoE finalize fused with all-reduce. Open: JIT softmax/argmax, a one-warp-per-token MoE router, and CuTe DSL NVFP4 fused MoE for SM100.
- **The scheduler/detokenizer IPC path is being slimmed.** Merged PRs send per-request stats and decode inputs once, use flat output-id columns, and remove PD multiplexing. The Rust server is gaining parity with the Python one (drain, abort, profile, cached-token stats).
- **PD disaggregation, HiCache and the KVCR direct linker are being hardened.** PP-stage agreement, host-sync-free KV destinations and unified page-envelope pools are merged. A large stack of open KVCR PRs is still in progress.
- **Direction:** push throughput on Blackwell and gfx950/gfx1250, move multimodal to a token-space pipeline (miles refactor 1–9), and reorganize CI tiers.

## Most important PRs
**[#46690](https://github.com/sgl-project/sglang/pull/46690) and [#46691](https://github.com/sgl-project/sglang/pull/46691) — MiniMax gfx950 kernel suites (merged).** Add gfx950 sparse attention with NVFP4 KV and DSpark verify kernels ([#46690](https://github.com/sgl-project/sglang/pull/46690)), plus MoE, router GEMV, block-fp8 GEMM and fp8 producer kernels ([#46691](https://github.com/sgl-project/sglang/pull/46691)). Together they are the main MiniMax M3 enablement on MI355-class hardware.

**[#47196](https://github.com/sgl-project/sglang/pull/47196) — Unlimited-OCR v2 model support (merged).** The largest feature this window, spanning 122 files across attention, multimodal, scheduler and CI.

**[#46857](https://github.com/sgl-project/sglang/pull/46857) — GLM-5.3 TP decode fusion with CP prefill (merged).** Restores TP decode fusion and graph sizing when context-parallel prefill is enabled, recovering a decode-path regression.

**[#44465](https://github.com/sgl-project/sglang/pull/44465) — DSv4.1 sharded accept on AMD (merged).** Removes the per-step whole-vocab gather of draft logits in speculative decoding, cutting communication and latency on every step.

**[#47589](https://github.com/sgl-project/sglang/pull/47589) — SM100 CuTe DSL NVFP4 kernels (open).** Adds DualGEMM+SwiGLU, PDL-safe GEMM, Grouped GEMM and fused MoE for Blackwell. It is the biggest new-kernel PR in flight, at over 20k lines.

## More changes by area

<details>
<summary>Performance (merged, 30)</summary>

- [#47260](https://github.com/sgl-project/sglang/pull/47260) send per-request decode inputs to the detokenizer once
- [#47415](https://github.com/sgl-project/sglang/pull/47415) flat output-id column with row offsets
- [#47178](https://github.com/sgl-project/sglang/pull/47178) send per-request output stats only when changed
- [#47166](https://github.com/sgl-project/sglang/pull/47166) typed scheduler timing reports to the tokenizer
- [#45328](https://github.com/sgl-project/sglang/pull/45328) publish PD decode KV destinations without host syncs
- [#47015](https://github.com/sgl-project/sglang/pull/47015) poll finished KV transfers during prefill wait
- [#46908](https://github.com/sgl-project/sglang/pull/46908) reuse fused QK-norm/RoPE kernel for Qwen3 decode
- [#46832](https://github.com/sgl-project/sglang/pull/46832) AMD Qwen3 fused QK-norm+RoPE+KV write with fp8 KV
- [#46724](https://github.com/sgl-project/sglang/pull/46724) fuse MoE finalize with 2shot_push all-reduce (muse-spark-open)
- [#47387](https://github.com/sgl-project/sglang/pull/47387) balance SM90 DSv4.1 paged decode indexer tiles
- [#46677](https://github.com/sgl-project/sglang/pull/46677) AMD DSv4.1 32x32-block fp8 wo_a GEMM
- [#47149](https://github.com/sgl-project/sglang/pull/47149) DSv4 amax8_varlen and mega MoE grids for 1024-thread SMs
- [#47304](https://github.com/sgl-project/sglang/pull/47304) drop per-layer routing glue under simulated routing with EPLB
- [#46024](https://github.com/sgl-project/sglang/pull/46024) mhc hc_combine_norm_mxfp8 row split by batch size
- [#46692](https://github.com/sgl-project/sglang/pull/46692) JIT quick all-reduce for TP4 on gfx950
- [#40708](https://github.com/sgl-project/sglang/pull/40708) aiter topk_gating for 512-expert Qwen3.5 routing
- [#41880](https://github.com/sgl-project/sglang/pull/41880) FlyDSL hc_mix for Qwen3.8 on gfx950
- [#37367](https://github.com/sgl-project/sglang/pull/37367) MoRI dispatch resolved from the AITER activation contract
- [#47180](https://github.com/sgl-project/sglang/pull/47180) replicate DCP query projection on the owned route
- [#46184](https://github.com/sgl-project/sglang/pull/46184) mamba conv verify window written as one tile
- [#44168](https://github.com/sgl-project/sglang/pull/44168) Cake softmax on SM100
- [#47070](https://github.com/sgl-project/sglang/pull/47070) H20 block-FP8 Triton configs for Qwen3-30B-A3B
- [#46731](https://github.com/sgl-project/sglang/pull/46731) MI355X fused MoE config for gemma-4-26B-A4B
- [#45295](https://github.com/sgl-project/sglang/pull/45295) detect hybrid SWA from layer_types
- [#45951](https://github.com/sgl-project/sglang/pull/45951) multi-LoRA serving under PP
- [#46500](https://github.com/sgl-project/sglang/pull/46500) LoRADrainer revamp
- [#42248](https://github.com/sgl-project/sglang/pull/42248) native tensor output and prefill scoring
- [#47550](https://github.com/sgl-project/sglang/pull/47550) forward metadata fill kernels
- [#47115](https://github.com/sgl-project/sglang/pull/47115) strided grid for padded MoE buffer rows
- [#46456](https://github.com/sgl-project/sglang/pull/46456), [#47452](https://github.com/sgl-project/sglang/pull/47452), [#46884](https://github.com/sgl-project/sglang/pull/46884), [#47161](https://github.com/sgl-project/sglang/pull/47161), [#47106](https://github.com/sgl-project/sglang/pull/47106) paged-experts pinning, Kimi-K3 NCCL residual banks, HiCache read-done, Rust frontend CPU pinning, egress logprob flattening
</details>

<details>
<summary>Diffusion performance (merged, 13)</summary>

- [#47121](https://github.com/sgl-project/sglang/pull/47121) Wan-Animate-2 1.7x faster denoising via exact FA3
- [#46454](https://github.com/sgl-project/sglang/pull/46454) HunyuanImage-3 prefix K/V cache and FA3
- [#46277](https://github.com/sgl-project/sglang/pull/46277) Wan-Animate-2 decode and LTX-2 closed-form fixes
- [#47569](https://github.com/sgl-project/sglang/pull/47569) MiniMax-H3 fast QK RMSNorm and fused RoPE on ROCm
- [#47567](https://github.com/sgl-project/sglang/pull/47567) MiniMax-H3 Ulysses exchange pipelined on RCCL
- [#47566](https://github.com/sgl-project/sglang/pull/47566) MiniMax-H3 skips attention for alignment rows
- [#47467](https://github.com/sgl-project/sglang/pull/47467) Qwen-Image-2.1 text encoder CUDA graph replay
- [#47465](https://github.com/sgl-project/sglang/pull/47465) Qwen-Image-2.1 Q/K norm+RoPE half-warp
- [#46722](https://github.com/sgl-project/sglang/pull/46722), [#46723](https://github.com/sgl-project/sglang/pull/46723) gfx1250 Wan VAE and scale-shift Triton
- [#46328](https://github.com/sgl-project/sglang/pull/46328), [#47686](https://github.com/sgl-project/sglang/pull/47686), [#47022](https://github.com/sgl-project/sglang/pull/47022), [#46028](https://github.com/sgl-project/sglang/pull/46028) Wan UMT5 padding trim, Nomas camera attention, joy-image GELU, cosmos3 GPU BLAKE3
</details>

<details>
<summary>Kernels & attention (merged, 6)</summary>

- [#47300](https://github.com/sgl-project/sglang/pull/47300) TensorMatcher device/dtype options and kDLGPU aliases
- [#47029](https://github.com/sgl-project/sglang/pull/47029) extend attention KV offsets in int64
- [#46833](https://github.com/sgl-project/sglang/pull/46833) aiter uses the layer's softmax scale
- [#47301](https://github.com/sgl-project/sglang/pull/47301) Blackwell subtile attention selection by mode
- [#35151](https://github.com/sgl-project/sglang/pull/35151) quantized diffusion attention for GFX942/GFX950
- [#45765](https://github.com/sgl-project/sglang/pull/45765) expose GLM5 MLA key buffer in binding
</details>

<details>
<summary>MoE & quantization (merged, 9)</summary>

- [#46018](https://github.com/sgl-project/sglang/pull/46018) humming adapted to kernels 0.1.18
- [#46212](https://github.com/sgl-project/sglang/pull/46212) NPU Qwen3.6-35B-A3B block-FP8 MoE
- [#46800](https://github.com/sgl-project/sglang/pull/46800) Quark MXFP8 shared experts kept out of the MXFP4 slot
- [#47408](https://github.com/sgl-project/sglang/pull/47408), [#41389](https://github.com/sgl-project/sglang/pull/41389) Quark MXFP4 W4A16 on gfx1151
- [#35955](https://github.com/sgl-project/sglang/pull/35955) gptq_marlin BF16 and act-order w2 scales
- [#45486](https://github.com/sgl-project/sglang/pull/45486) CT FP8 Triton layout on AMD
- [#47577](https://github.com/sgl-project/sglang/pull/47577) megamoe symmetric buffers allocated before KV sizing
- [#44750](https://github.com/sgl-project/sglang/pull/44750) nemotron-h CuTe DSL W4A16 MoE
</details>

<details>
<summary>Model support (merged, 9)</summary>

- [#46780](https://github.com/sgl-project/sglang/pull/46780) Rust parser for DeepSeek-V4/V4.1 output
- [#47411](https://github.com/sgl-project/sglang/pull/47411) native Gemma-4-Unified encoder for LTX-2.5
- [#47378](https://github.com/sgl-project/sglang/pull/47378) Pika-H3-Flex (MiniMax-H3 + LoRA)
- [#44442](https://github.com/sgl-project/sglang/pull/44442) NPU GLM-4.1V ModelSlim W8A8S
- [#39947](https://github.com/sgl-project/sglang/pull/39947) NPU DSv4 DSpark on Ascend 950
- [#46278](https://github.com/sgl-project/sglang/pull/46278) NPU DSpark native sampling and verification
- [#44200](https://github.com/sgl-project/sglang/pull/44200) watermark with DSPARK
- [#47135](https://github.com/sgl-project/sglang/pull/47135) LoRA upsert on /load_lora_adapter
- [#47615](https://github.com/sgl-project/sglang/pull/47615) GLM-5.2 MI355X recipe
</details>

<details>
<summary>Parallelism & scheduling (merged, 16)</summary>

- [#43898](https://github.com/sgl-project/sglang/pull/43898) remove PD multiplexing
- [#43895](https://github.com/sgl-project/sglang/pull/43895), [#43896](https://github.com/sgl-project/sglang/pull/43896), [#43899](https://github.com/sgl-project/sglang/pull/43899), [#43900](https://github.com/sgl-project/sglang/pull/43900) scheduler state routed through Req, ReqKvInfo and owner-list methods
- [#47544](https://github.com/sgl-project/sglang/pull/47544) PD handoff token commit
- [#46395](https://github.com/sgl-project/sglang/pull/46395) decode KV written to the linker, already-stored pages skipped
- [#47124](https://github.com/sgl-project/sglang/pull/47124) decode host receive on page-envelope pool
- [#47063](https://github.com/sgl-project/sglang/pull/47063), [#47045](https://github.com/sgl-project/sglang/pull/47045) PP-stage agreement on KV transfer outcome
- [#46373](https://github.com/sgl-project/sglang/pull/46373), [#43299](https://github.com/sgl-project/sglang/pull/43299), [#47366](https://github.com/sgl-project/sglang/pull/47366), [#47638](https://github.com/sgl-project/sglang/pull/47638) PD transfer, early-send, rebootstrap and aux_item_lens fixes
- [#45434](https://github.com/sgl-project/sglang/pull/45434) CP KV layout hooks
- [#38943](https://github.com/sgl-project/sglang/pull/38943) breakable prefill CUDA graphs under DCP
- [#46827](https://github.com/sgl-project/sglang/pull/46827) joint_lru for Full and SWA KV
</details>

<details>
<summary>Rust server (merged, 12)</summary>

- [#47489](https://github.com/sgl-project/sglang/pull/47489) drain on SIGTERM
- [#47321](https://github.com/sgl-project/sglang/pull/47321) end aborted request on the scheduler's abort reason
- [#46949](https://github.com/sgl-project/sglang/pull/46949) customized_info in native /generate
- [#46961](https://github.com/sgl-project/sglang/pull/46961) cached tokens by tier in meta_info
- [#46963](https://github.com/sgl-project/sglang/pull/46963) per-request scheduler stats in meta_info
- [#46968](https://github.com/sgl-project/sglang/pull/46968) /start_profile and /stop_profile
- [#47112](https://github.com/sgl-project/sglang/pull/47112) request, headers and outcome in generate hook
- [#47169](https://github.com/sgl-project/sglang/pull/47169) launch-time fields in /model_info
- [#47532](https://github.com/sgl-project/sglang/pull/47532) aborts to every attention-DP rank
- [#47108](https://github.com/sgl-project/sglang/pull/47108), [#47319](https://github.com/sgl-project/sglang/pull/47319), [#47691](https://github.com/sgl-project/sglang/pull/47691), [#47113](https://github.com/sgl-project/sglang/pull/47113), [#45996](https://github.com/sgl-project/sglang/pull/45996) MM readiness, /v1/loads, listener validation, metrics race, DP listener ports
</details>

<details>
<summary>Multimodal refactor (merged, 10)</summary>

- [#46680](https://github.com/sgl-project/sglang/pull/46680) through [#46699](https://github.com/sgl-project/sglang/pull/46699) and [#46729](https://github.com/sgl-project/sglang/pull/46729) shared enums, mixin, transport split and token-space processor (refactor 1/9 to 5/9)
- [#46753](https://github.com/sgl-project/sglang/pull/46753) token-space processor behind a flag
- [#46767](https://github.com/sgl-project/sglang/pull/46767) Qwen VL token-space strategy
- [#46768](https://github.com/sgl-project/sglang/pull/46768) check Qwen token-space output against legacy
- [#46769](https://github.com/sgl-project/sglang/pull/46769) expand only the new turn
- [#47358](https://github.com/sgl-project/sglang/pull/47358), [#47355](https://github.com/sgl-project/sglang/pull/47355) strategy media/video hooks and registry
</details>

<details>
<summary>Hardware & arch (merged, 8)</summary>

- [#46623](https://github.com/sgl-project/sglang/pull/46623) consolidate XPU enablements
- [#42725](https://github.com/sgl-project/sglang/pull/42725) Intel XPU page_size=1
- [#44718](https://github.com/sgl-project/sglang/pull/44718) AMD mamba hicache checkpoints without GPU slot
- [#45302](https://github.com/sgl-project/sglang/pull/45302) NPU DSA sparse offload budgeting
- [#47380](https://github.com/sgl-project/sglang/pull/47380) NPU docs renamed to A2/A3
- [#46883](https://github.com/sgl-project/sglang/pull/46883) uTLX in gfx950 rocm10 images
- [#46685](https://github.com/sgl-project/sglang/pull/46685) daily sgl-amd-mono pin bump
- [#47056](https://github.com/sgl-project/sglang/pull/47056) XPU GSM8K tests moved to sgl-eval
</details>

<details>
<summary>API & serving (merged, 10)</summary>

- [#47087](https://github.com/sgl-project/sglang/pull/47087) RL check_weights hashes raw received weights
- [#47085](https://github.com/sgl-project/sglang/pull/47085) RL prompt KV weight versions in metadata
- [#47320](https://github.com/sgl-project/sglang/pull/47320) RL byte-range reads of output store
- [#47086](https://github.com/sgl-project/sglang/pull/47086) kv-canary passthrough
- [#47072](https://github.com/sgl-project/sglang/pull/47072) typed customized_info values
- [#47159](https://github.com/sgl-project/sglang/pull/47159) TTFT phase breakdown in meta_info
- [#47353](https://github.com/sgl-project/sglang/pull/47353) FPM multiple timing listeners
- [#46882](https://github.com/sgl-project/sglang/pull/46882) and [#47198](https://github.com/sgl-project/sglang/pull/47198) grpc media inputs, plus release cherry-pick
- [#47055](https://github.com/sgl-project/sglang/pull/47055) cancel diffusion video jobs on DELETE
- [#39880](https://github.com/sgl-project/sglang/pull/39880) HiCache fast_file backend
</details>

<details>
<summary>Bugfixes (merged, 35)</summary>

- [#46720](https://github.com/sgl-project/sglang/pull/46720) keep attention metadata alive across CUDA graph variants
- [#46737](https://github.com/sgl-project/sglang/pull/46737) release storage held by empty break inputs
- [#45839](https://github.com/sgl-project/sglang/pull/45839) HiCache KDA load events
- [#43110](https://github.com/sgl-project/sglang/pull/43110) hicache sidecars
- [#47543](https://github.com/sgl-project/sglang/pull/47543), [#47557](https://github.com/sgl-project/sglang/pull/47557) hicache mlock and page-cache credit
- [#47716](https://github.com/sgl-project/sglang/pull/47716) early result processing ordering
- [#47521](https://github.com/sgl-project/sglang/pull/47521) abort retracted requests that cannot be rebuilt
- [#47546](https://github.com/sgl-project/sglang/pull/47546) do not dispatch a request already aborted
- [#47445](https://github.com/sgl-project/sglang/pull/47445) msgpack IPC dtype round-trip
- [#47333](https://github.com/sgl-project/sglang/pull/47333) ragged-verify eager fallback
- [#46840](https://github.com/sgl-project/sglang/pull/46840) DSPARK verify accept cost
- [#38565](https://github.com/sgl-project/sglang/pull/38565) deterministic top-p/top-k renorm under TP
- [#45174](https://github.com/sgl-project/sglang/pull/45174) MiniMax-M3 radix top-k tie-breaking
- [#44268](https://github.com/sgl-project/sglang/pull/44268) fused MoE sum all-reduce
- [#46625](https://github.com/sgl-project/sglang/pull/46625) MSA plugin behind megakernel flag
- [#45496](https://github.com/sgl-project/sglang/pull/45496) DP controller round-robin
- [#47545](https://github.com/sgl-project/sglang/pull/47545) redact watermark keys
- [#44316](https://github.com/sgl-project/sglang/pull/44316) PyO3 0.29
- [#47107](https://github.com/sgl-project/sglang/pull/47107) crash-dump writer
- [#40107](https://github.com/sgl-project/sglang/pull/40107) customized_info across PD
- Diffusion fixes: [#47488](https://github.com/sgl-project/sglang/pull/47488), [#47240](https://github.com/sgl-project/sglang/pull/47240), [#47092](https://github.com/sgl-project/sglang/pull/47092), [#47270](https://github.com/sgl-project/sglang/pull/47270), [#45065](https://github.com/sgl-project/sglang/pull/45065), [#45834](https://github.com/sgl-project/sglang/pull/45834), [#45837](https://github.com/sgl-project/sglang/pull/45837), [#46255](https://github.com/sgl-project/sglang/pull/46255), [#46274](https://github.com/sgl-project/sglang/pull/46274), [#46601](https://github.com/sgl-project/sglang/pull/46601), [#47571](https://github.com/sgl-project/sglang/pull/47571), [#47582](https://github.com/sgl-project/sglang/pull/47582)
</details>

<details>
<summary>Tests, CI & docs (merged, 20)</summary>

- [#45981](https://github.com/sgl-project/sglang/pull/45981) LoRA tests simplified with a rerun group
- [#46721](https://github.com/sgl-project/sglang/pull/46721) CUDA-graph lifetime validation tool
- [#47603](https://github.com/sgl-project/sglang/pull/47603) drop tests that never run in CI
- [#47619](https://github.com/sgl-project/sglang/pull/47619) CUDA tests re-tiered
- [#46627](https://github.com/sgl-project/sglang/pull/46627) MiniMax-M3.1 nightly e2e on H200 and B300
- [#47162](https://github.com/sgl-project/sglang/pull/47162), [#47246](https://github.com/sgl-project/sglang/pull/47246) AMD CI spread, CPU CI result comment
- [#46394](https://github.com/sgl-project/sglang/pull/46394) XPU rolling tag
- [#47723](https://github.com/sgl-project/sglang/pull/47723) CI skills updated
- Cookbook and docs: [#47214](https://github.com/sgl-project/sglang/pull/47214), [#47464](https://github.com/sgl-project/sglang/pull/47464), [#47623](https://github.com/sgl-project/sglang/pull/47623), [#47699](https://github.com/sgl-project/sglang/pull/47699), [#47303](https://github.com/sgl-project/sglang/pull/47303), [#47560](https://github.com/sgl-project/sglang/pull/47560), [#47212](https://github.com/sgl-project/sglang/pull/47212), [#45683](https://github.com/sgl-project/sglang/pull/45683)
- plus 4 more minor items
</details>

<details>
<summary>Refactors (merged, 8)</summary>

- [#45019](https://github.com/sgl-project/sglang/pull/45019), [#44990](https://github.com/sgl-project/sglang/pull/44990), [#40916](https://github.com/sgl-project/sglang/pull/40916), [#45020](https://github.com/sgl-project/sglang/pull/45020), [#40914](https://github.com/sgl-project/sglang/pull/40914), [#47705](https://github.com/sgl-project/sglang/pull/47705) memory-pool buffer-info and layout renames
- [#47338](https://github.com/sgl-project/sglang/pull/47338) incremental detokenizer move
- [#34038](https://github.com/sgl-project/sglang/pull/34038) ragged-verify graph tier
</details>

<details>
<summary>Open PRs (in progress, notable)</summary>

- [#47589](https://github.com/sgl-project/sglang/pull/47589), [#47641](https://github.com/sgl-project/sglang/pull/47641), [#47784](https://github.com/sgl-project/sglang/pull/47784) SM100 NVFP4 CuTe DSL fused MoE, one-warp MoE router, JIT moe_finalize_fuse_shared
- [#47469](https://github.com/sgl-project/sglang/pull/47469), [#47666](https://github.com/sgl-project/sglang/pull/47666), [#47210](https://github.com/sgl-project/sglang/pull/47210), [#47658](https://github.com/sgl-project/sglang/pull/47658), [#47672](https://github.com/sgl-project/sglang/pull/47672), [#47741](https://github.com/sgl-project/sglang/pull/47741) DSv4.1 LiteTopK indexer top-k, SM90 FP4 scoring, SM120 DeepGEMM, hc-prenorm, CP compressor, prefill graphs
- [#47597](https://github.com/sgl-project/sglang/pull/47597), [#47748](https://github.com/sgl-project/sglang/pull/47748) DSv4.1 DP attention with CP prefill, deterministic sparse top-k
- [#47660](https://github.com/sgl-project/sglang/pull/47660), [#47421](https://github.com/sgl-project/sglang/pull/47421), [#47635](https://github.com/sgl-project/sglang/pull/47635), [#47720](https://github.com/sgl-project/sglang/pull/47720) DSv4.1 on Ascend A5 and Xeon CPU, DSv4 sparse offload and prefill query bounds on NPU
- [#47271](https://github.com/sgl-project/sglang/pull/47271) Mistral-Large-4
- [#47371](https://github.com/sgl-project/sglang/pull/47371), [#47633](https://github.com/sgl-project/sglang/pull/47633) MiniMax M3.1 NVFP4 DeepEP, muse-spark ROCm day0
- [#47200](https://github.com/sgl-project/sglang/pull/47200), [#47201](https://github.com/sgl-project/sglang/pull/47201), [#47324](https://github.com/sgl-project/sglang/pull/47324), [#47512](https://github.com/sgl-project/sglang/pull/47512), [#47765](https://github.com/sgl-project/sglang/pull/47765) speculative-decode fast paths, EAGLE launches, JIT softmax, DFlash fused overwrite
- [#47318](https://github.com/sgl-project/sglang/pull/47318), [#47317](https://github.com/sgl-project/sglang/pull/47317), [#47694](https://github.com/sgl-project/sglang/pull/47694), [#47359](https://github.com/sgl-project/sglang/pull/47359), [#47376](https://github.com/sgl-project/sglang/pull/47376) DSpark DSv4.1 launches, ROCm verify, padding-row accept fix, DSpine, Spark2.5
- [#47674](https://github.com/sgl-project/sglang/pull/47674), [#47402](https://github.com/sgl-project/sglang/pull/47402), [#47528](https://github.com/sgl-project/sglang/pull/47528) token-space strategies for GLM-5.3 and Qwen-VL on miles
- [#47535](https://github.com/sgl-project/sglang/pull/47535), [#47514](https://github.com/sgl-project/sglang/pull/47514), [#47681](https://github.com/sgl-project/sglang/pull/47681), [#47682](https://github.com/sgl-project/sglang/pull/47682) KVCR direct-linker stack
- [#47777](https://github.com/sgl-project/sglang/pull/47777), [#47775](https://github.com/sgl-project/sglang/pull/47775), [#47774](https://github.com/sgl-project/sglang/pull/47774), [#47776](https://github.com/sgl-project/sglang/pull/47776), [#47342](https://github.com/sgl-project/sglang/pull/47342) AMD GDN and KDA prefill work on gfx950
- [#47219](https://github.com/sgl-project/sglang/pull/47219), [#47278](https://github.com/sgl-project/sglang/pull/47278), [#47276](https://github.com/sgl-project/sglang/pull/47276), [#47241](https://github.com/sgl-project/sglang/pull/47241) AMD FlyDSL QR int4, DSA decode and indexer work
- [#47600](https://github.com/sgl-project/sglang/pull/47600) NCCL EP a2a backend
- [#47383](https://github.com/sgl-project/sglang/pull/47383), [#47588](https://github.com/sgl-project/sglang/pull/47588) HiSparse and sail DeepGEMM backends
- [#47731](https://github.com/sgl-project/sglang/pull/47731), [#47782](https://github.com/sgl-project/sglang/pull/47782), [#47806](https://github.com/sgl-project/sglang/pull/47806) import slimming, GPU-arch query centralization, CI est_time update
- plus about 380 more open PRs not listed
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 99fd1f44c4bc7ee225cc1e74a41364da20f3c61bea296cd25205c4337e8d60fd -->
