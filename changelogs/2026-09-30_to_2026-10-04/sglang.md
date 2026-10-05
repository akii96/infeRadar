# sglang: PR digest (2026-09-30 to 2026-10-04)

_302 merged, 466 newly opened - source sgl-project/sglang, generated 2026-10-05T00:27:17Z_

## TL;DR
- **DeepSeek V4.1 got the most attention** (70 PRs), with merged perf work on Hopper/Blackwell (`[#41251](https://github.com/sgl-project/sglang/pull/41251)`, `[#41660](https://github.com/sgl-project/sglang/pull/41660)`, `[#41658](https://github.com/sgl-project/sglang/pull/41658)`, `[#41657](https://github.com/sgl-project/sglang/pull/41657)`) and a large gfx950 enablement on AMD (`[#41308](https://github.com/sgl-project/sglang/pull/41308)`, plus the OPUS sparse prefill, MXFP8 GEMM and shared-expert fusion follow-ups). Newly opened PDMux PRs add layerwise MTP/DSpark and bounded layerwise prefill for V4.1-Flash.
- **GLM and MiniMax-M3 were the other focus models**, mostly on ROCm: a fused DSA indexer decode path (`[#38583](https://github.com/sgl-project/sglang/pull/38583)`), decode-shaped MoE/MLA tiles (`[#41725](https://github.com/sgl-project/sglang/pull/41725)`), and FP8/MXFP4 serving (`[#39273](https://github.com/sgl-project/sglang/pull/39273)`). MiniMax-M3 got AITER ASM prefill and TP4 indexer partitioning.
- **Qwen 3.8 / QSA and linear attention**: fused NEXTN verify and graph-input prep, QSA KV prep fusion, and CP for QSA attention. KDA's `ptx_kda` prefill now runs on SM100.
- **Direction**: an architecture cleanup (attn-DP flag, stage-boundary decoders, parallel-context refactors), a unified-memory KV pool series (1/7 to 7/7), and a Router/PD hardening push. Newly opened work is dominated by a huge LoRA 1-17 stack, the cake_kernels adapter and route stack, and TCPCG retirement.

## Most important PRs
**`[#41308](https://github.com/sgl-project/sglang/pull/41308)` DeepSeek-V4.1 on gfx950 (AMD)**
End-to-end serving enablement across attention, MLA, MoE, quantization and speculative decoding. It is the foundation for the many AMD V4.1 follow-ups this window.

**`[#41251](https://github.com/sgl-project/sglang/pull/41251)` DeepSeek V4.1 Flash Hopper paths and Blackwell prefill selection**
Optimizes the Hopper attention, MoE and quantization paths and improves prefill kernel selection on Blackwell. It is the biggest NVIDIA-side V4.1 perf change.

**`[#38583](https://github.com/sgl-project/sglang/pull/38583)` GLM-5.2 fused DSA indexer decode on gfx950**
Four-kernel fused indexer decode path for the sparse-attention indexer, which dominates decode cost on this model.

**`[#41818](https://github.com/sgl-project/sglang/pull/41818)` `--attn-dp-size` replaces `--enable-dp-attention`**
Touches 366 files. It turns attention data parallelism into a sized parallel dimension and deprecates the boolean flag.

**`[#41175](https://github.com/sgl-project/sglang/pull/41175)` Qwen 3.8 NEXTN fused verify/draft input prep**
Fuses graph-input preparation for the verify and draft steps, cutting launch overhead in the speculative-decoding hot loop.

## More changes by area

<details>
<summary>Performance (6)</summary>

- [#41660](https://github.com/sgl-project/sglang/pull/41660) fused c1/c2 compress for eager extend, faster c2 decode (DSv4.1)
- [#41658](https://github.com/sgl-project/sglang/pull/41658) faster fp4 index-K gather and combine_topk_swa_indices
- [#41459](https://github.com/sgl-project/sglang/pull/41459) faster LTX-2.3 QK norm and split RoPE on H200
- [#41711](https://github.com/sgl-project/sglang/pull/41711) diffusion perf dump: one writer per replica
- [#41834](https://github.com/sgl-project/sglang/pull/41834) Wan: encode the MP4 while the VAE decodes
- [#42479](https://github.com/sgl-project/sglang/pull/42479) fused MoE finalize all-reduce only offered where the sum is owed

</details>

<details>
<summary>Kernels & attention (16)</summary>

- [#41657](https://github.com/sgl-project/sglang/pull/41657) fold q_rope_store into fused_q_norm_rope (DSv4.1)
- [#40972](https://github.com/sgl-project/sglang/pull/40972) fuse QSA KV preparation and sparse block expansion
- [#41173](https://github.com/sgl-project/sglang/pull/41173) fuse QSA graph replay metadata across draft steps
- [#39721](https://github.com/sgl-project/sglang/pull/39721) CP for QSA attention and sparse indexer
- [#39614](https://github.com/sgl-project/sglang/pull/39614) optional fp8 storage for the compressed QSA indexer cache
- [#41445](https://github.com/sgl-project/sglang/pull/41445) enable ptx_kda prefill on SM100
- [#41572](https://github.com/sgl-project/sglang/pull/41572) fix ptx_kda prefill NaN without a gate lower bound
- [#42251](https://github.com/sgl-project/sglang/pull/42251) opt-in decode-parity mode for Triton KDA recurrence
- [#42486](https://github.com/sgl-project/sglang/pull/42486) explicit reciprocal scaling for recurrent Q/K norm
- [#40227](https://github.com/sgl-project/sglang/pull/40227) expose GDN/KDA prefill hooks
- [#39130](https://github.com/sgl-project/sglang/pull/39130) triton autotune on Mamba2 SSD kernels
- [#41336](https://github.com/sgl-project/sglang/pull/41336) expose FlashMLA kv_format in sparse decode
- [#42004](https://github.com/sgl-project/sglang/pull/42004) Cake softmax for SM103 sampling
- [#39931](https://github.com/sgl-project/sglang/pull/39931) ROCm topk v2 splits one long row across blocks
- [#38187](https://github.com/sgl-project/sglang/pull/38187) Llama4 local attention page ids in CUDA-graph capture
- [#42036](https://github.com/sgl-project/sglang/pull/42036) PCP: remove CP adapter, separate interleave transport from boundary reduction

</details>

<details>
<summary>MoE & quantization (12)</summary>

- [#38040](https://github.com/sgl-project/sglang/pull/38040) ConvRot INT8 online W8A8 for DiTs
- [#41671](https://github.com/sgl-project/sglang/pull/41671) fuse Flux3 rowwise FP8 quant with Triton
- [#39818](https://github.com/sgl-project/sglang/pull/39818) FlashInfer A2A for MoE prefill instead of AG+RS
- [#41759](https://github.com/sgl-project/sglang/pull/41759) keep moe_align_block_size pad fill inside sorted_token_ids
- [#41807](https://github.com/sgl-project/sglang/pull/41807) shard WNA16 and Quark INT4-FP8 MoE weights by MoE placement
- [#42011](https://github.com/sgl-project/sglang/pull/42011) AMD V4.1 shared-expert fusion accuracy and MoE routing speed
- [#41870](https://github.com/sgl-project/sglang/pull/41870) GLM-5.3-Flash shared expert and KDA projection fusion on Quark MXFP4
- [#41970](https://github.com/sgl-project/sglang/pull/41970) gfx950 fp8 dense GEMMs switched to aiter MXFP8
- [#42055](https://github.com/sgl-project/sglang/pull/42055) fuse MXFP8 activation quant into producer kernels
- [#40811](https://github.com/sgl-project/sglang/pull/40811) Kimi-K3 MXFP4 on ROCm
- [#39618](https://github.com/sgl-project/sglang/pull/39618) XPU dynamic_expert_bias and track_state
- [#40190](https://github.com/sgl-project/sglang/pull/40190) XPU fused QK-norm + RoPE for Qwen3-MoE

</details>

<details>
<summary>Model support (8)</summary>

- [#41488](https://github.com/sgl-project/sglang/pull/41488) MiniMax-M3 TP4 indexer context partitioning (AMD)
- [#41707](https://github.com/sgl-project/sglang/pull/41707) AITER ASM prefill for MiniMax-M3 HD128
- [#35357](https://github.com/sgl-project/sglang/pull/35357) MiniMax-M3 fused sparse QK norm, RoPE and cache writes
- [#34365](https://github.com/sgl-project/sglang/pull/34365) MiniMax H3 RL diffusion support
- [#34201](https://github.com/sgl-project/sglang/pull/34201) top-p mask capture for spec, DFlash/DSpark
- [#41986](https://github.com/sgl-project/sglang/pull/41986) NVFP4 checkpoint in GLM-5.3-Flash cookbook
- [#42174](https://github.com/sgl-project/sglang/pull/42174) Qwen-Image 2.1 fused gate_up LoRAs
- [#42171](https://github.com/sgl-project/sglang/pull/42171) FLUX 3 Action CUDA graphs

</details>

<details>
<summary>Parallelism & scheduling (14)</summary>

- [#37787](https://github.com/sgl-project/sglang/pull/37787) NPU decode context parallel for DSA models
- [#42038](https://github.com/sgl-project/sglang/pull/42038) DP x TP x CP with interleave CP
- [#42041](https://github.com/sgl-project/sglang/pull/42041) scattered interleave CP inputs with EP
- [#34200](https://github.com/sgl-project/sglang/pull/34200) CP V2 for DeepSeek-V4 HIP backend
- [#40001](https://github.com/sgl-project/sglang/pull/40001) fix hybrid recurrent state under PP x spec decode
- [#41950](https://github.com/sgl-project/sglang/pull/41950) scheduler internal-state readback moved to a collaborator
- [#42025](https://github.com/sgl-project/sglang/pull/42025) label scheduler stage time by sampled forward overlap
- [#42035](https://github.com/sgl-project/sglang/pull/42035) keep ingesting requests while prefill result is pending
- [#37077](https://github.com/sgl-project/sglang/pull/37077) centralize drain-aware PD abort acks
- [#40703](https://github.com/sgl-project/sglang/pull/40703) opt-in prefill-complete decode KV allocation
- [#42051](https://github.com/sgl-project/sglang/pull/42051) validate PD decode state layout at registration
- [#41607](https://github.com/sgl-project/sglang/pull/41607) validate state strides before Mooncake transfers
- [#37827](https://github.com/sgl-project/sglang/pull/37827) NIXL stride desc API
- [#41786](https://github.com/sgl-project/sglang/pull/41786) publish prefill DP rank when forced lookup enabled

</details>

<details>
<summary>Hardware & arch (10)</summary>

- [#39166](https://github.com/sgl-project/sglang/pull/39166) PD-disagg with fp8 unified_kv on gfx950
- [#42017](https://github.com/sgl-project/sglang/pull/42017) OPUS sparse prefill on gfx950
- [#41981](https://github.com/sgl-project/sglang/pull/41981) greedy dspark draft/accept under SGLANG_SIMULATE_ACC_LEN
- [#42014](https://github.com/sgl-project/sglang/pull/42014) DSpark draft metadata inside the CUDA graph on ROCm
- [#41947](https://github.com/sgl-project/sglang/pull/41947) low-ratio indexer top-k via top-k v2
- [#41513](https://github.com/sgl-project/sglang/pull/41513) QSA packed-varlen decode to aiter on HIP
- [#40750](https://github.com/sgl-project/sglang/pull/40750) AITER MLA DCP decode ASM path
- [#34438](https://github.com/sgl-project/sglang/pull/34438) aiter asm ps for Kimi K3 prefill
- [#36780](https://github.com/sgl-project/sglang/pull/36780) Apple Silicon (MPS) platform
- [#41717](https://github.com/sgl-project/sglang/pull/41717) Kimi-K3 NPU PD disaggregation recipes

</details>

<details>
<summary>Unified memory & HiCache (16)</summary>

- [#40326](https://github.com/sgl-project/sglang/pull/40326) derive KV row addresses from strides (1/7)
- [#40327](https://github.com/sgl-project/sglang/pull/40327) build paged KV views through one helper (2/7)
- [#38592](https://github.com/sgl-project/sglang/pull/38592) token-major dense views (3/7)
- [#40328](https://github.com/sgl-project/sglang/pull/40328) mark write loc physical (4/7)
- [#40329](https://github.com/sgl-project/sglang/pull/40329) remove kernel-page multiplier plumbing (5/7)
- [#40330](https://github.com/sgl-project/sglang/pull/40330) stride the KV translate kernel (6/7)
- [#40331](https://github.com/sgl-project/sglang/pull/40331) name the fused KV translate (7/7)
- [#41961](https://github.com/sgl-project/sglang/pull/41961) post-capture KV sizing for hybrid-SWA pool
- [#42252](https://github.com/sgl-project/sglang/pull/42252) copy page envelopes in place during compaction
- [#39479](https://github.com/sgl-project/sglang/pull/39479) fix unified HiCache physical transfers
- [#40913](https://github.com/sgl-project/sglang/pull/40913) HiCache host pools for DSA indexer
- [#41265](https://github.com/sgl-project/sglang/pull/41265) MLA DCP with Mooncake HiCache L3
- [#42125](https://github.com/sgl-project/sglang/pull/42125) size VMM graph-input exchange by widest input
- [#41128](https://github.com/sgl-project/sglang/pull/41128) deferred decode KV release metrics
- [#41520](https://github.com/sgl-project/sglang/pull/41520) rename cache_unfinished_req to checkpoint_req
- [#42202](https://github.com/sgl-project/sglang/pull/42202) rename insert_req to checkpoint

</details>

<details>
<summary>API & serving (22)</summary>

- [#42147](https://github.com/sgl-project/sglang/pull/42147) router native /generate
- [#42191](https://github.com/sgl-project/sglang/pull/42191) router /v1/embeddings
- [#42205](https://github.com/sgl-project/sglang/pull/42205) router /v1/rerank
- [#42258](https://github.com/sgl-project/sglang/pull/42258) router /v1/classify
- [#42183](https://github.com/sgl-project/sglang/pull/42183) /v1/systemone decision checkpoints
- [#41766](https://github.com/sgl-project/sglang/pull/41766) Rust gRPC adapter for native generation
- [#41964](https://github.com/sgl-project/sglang/pull/41964) wire gRPC server into frontend lifecycle
- [#41896](https://github.com/sgl-project/sglang/pull/41896) sglang-processor lib
- [#41726](https://github.com/sgl-project/sglang/pull/41726) shared runtime.v1 protobuf bindings
- [#41613](https://github.com/sgl-project/sglang/pull/41613) enforce compatible PD version groups
- [#41612](https://github.com/sgl-project/sglang/pull/41612) fail fast and cancel decode when prefill fails
- [#41611](https://github.com/sgl-project/sglang/pull/41611) load-only routing without tokenizer
- [#41610](https://github.com/sgl-project/sglang/pull/41610) exclude portless prefills, retry bootstrap discovery
- [#41974](https://github.com/sgl-project/sglang/pull/41974) --dp-aware routing to a DP rank
- [#41990](https://github.com/sgl-project/sglang/pull/41990) unify reorg session and cache affinity modes
- [#41996](https://github.com/sgl-project/sglang/pull/41996) --worker-api-key support
- [#42275](https://github.com/sgl-project/sglang/pull/42275) repair KV-event sequence gaps
- [#42276](https://github.com/sgl-project/sglang/pull/42276) credit routed prompts before KV events arrive
- [#42274](https://github.com/sgl-project/sglang/pull/42274) advertise KV-event replay endpoint
- [#42190](https://github.com/sgl-project/sglang/pull/42190) forward text where engine tokenizer differs
- [#40694](https://github.com/sgl-project/sglang/pull/40694), [#40695](https://github.com/sgl-project/sglang/pull/40695), [#40696](https://github.com/sgl-project/sglang/pull/40696), [#40697](https://github.com/sgl-project/sglang/pull/40697), [#40698](https://github.com/sgl-project/sglang/pull/40698), [#40699](https://github.com/sgl-project/sglang/pull/40699) router peer-bootstrap series (8-13 of 13)

</details>

<details>
<summary>Bugfixes (28)</summary>

- [#39982](https://github.com/sgl-project/sglang/pull/39982) unified-memory compaction gates and pending page reuse
- [#38229](https://github.com/sgl-project/sglang/pull/38229) Inkling unified-memory checkpoint destinations
- [#42072](https://github.com/sgl-project/sglang/pull/42072) unified-memory lazy checkpoint policy
- [#38480](https://github.com/sgl-project/sglang/pull/38480) HiCache host lock ownership across radix splits
- [#42264](https://github.com/sgl-project/sglang/pull/42264) HiCache write-back SWA insert assert
- [#42420](https://github.com/sgl-project/sglang/pull/42420) HiCache cgroup page-cache accounting
- [#42120](https://github.com/sgl-project/sglang/pull/42120) HiCache host-memory fallback without cgroup fs
- [#39862](https://github.com/sgl-project/sglang/pull/39862) HiCache Mamba slot side states
- [#39893](https://github.com/sgl-project/sglang/pull/39893) preserve QSA indexer state through HiCache
- [#31808](https://github.com/sgl-project/sglang/pull/31808) LoRA usage-counter accounting
- [#42005](https://github.com/sgl-project/sglang/pull/42005) NIXL dlists for DeepSeek-V4 KV entries
- [#41924](https://github.com/sgl-project/sglang/pull/41924) block scale registration for mixed full/SWA KV dtypes
- [#41346](https://github.com/sgl-project/sglang/pull/41346) return HiSparse slots on PD abort
- [#40471](https://github.com/sgl-project/sglang/pull/40471) DSV4 fp8 unified_kv rope pool linker
- [#41497](https://github.com/sgl-project/sglang/pull/41497) MiniMax-M3 EAGLE3 verify on ROCm
- [#41154](https://github.com/sgl-project/sglang/pull/41154) Qwen3.5 EAGLE3 capture and streaming overlap
- [#41789](https://github.com/sgl-project/sglang/pull/41789) Responses reasoning content-part events
- [#40077](https://github.com/sgl-project/sglang/pull/40077) preserve inline instructions for Responses/Kimi K3
- [#41838](https://github.com/sgl-project/sglang/pull/41838) namespace census at read leaf
- [#41810](https://github.com/sgl-project/sglang/pull/41810) Solar model constructible
- [#41754](https://github.com/sgl-project/sglang/pull/41754) Step-3.5 shared expert under all-to-all MoE
- [#42303](https://github.com/sgl-project/sglang/pull/42303) EXAONE/ERNIE 4.5 VL MoE issues
- [#42347](https://github.com/sgl-project/sglang/pull/42347) skip draft decode recapture without decode graph
- [#42346](https://github.com/sgl-project/sglang/pull/42346) draft tensor weight update from deployment TP rank
- [#41809](https://github.com/sgl-project/sglang/pull/41809) prefill delayer gather buffer sizing
- [#42480](https://github.com/sgl-project/sglang/pull/42480) GigaChat 3.5 stage boundaries built once
- [#41805](https://github.com/sgl-project/sglang/pull/41805) TensorCast WORLD placement names
- [#42494](https://github.com/sgl-project/sglang/pull/42494) AMD RoPE cache dtype and diffusion CI failures
- plus [#42121](https://github.com/sgl-project/sglang/pull/42121), [#42255](https://github.com/sgl-project/sglang/pull/42255), [#42436](https://github.com/sgl-project/sglang/pull/42436), [#42471](https://github.com/sgl-project/sglang/pull/42471), [#41025](https://github.com/sgl-project/sglang/pull/41025), [#42512](https://github.com/sgl-project/sglang/pull/42512) (diffusion, AMD, docs fixes)

</details>

<details>
<summary>Refactors (22)</summary>

- [#41750](https://github.com/sgl-project/sglang/pull/41750) rename layer boundary protocols and helpers
- [#42481](https://github.com/sgl-project/sglang/pull/42481) build layer stacks in order with append_stages
- [#42348](https://github.com/sgl-project/sglang/pull/42348) placement consumers read the parallel context
- [#42301](https://github.com/sgl-project/sglang/pull/42301) stage boundaries complete every stage-output sum
- [#42312](https://github.com/sgl-project/sglang/pull/42312) drop reduction-skip mechanisms
- [#42300](https://github.com/sgl-project/sglang/pull/42300) drop unused TBO op methods
- [#41778](https://github.com/sgl-project/sglang/pull/41778) simplify layer boundary internals
- [#41813](https://github.com/sgl-project/sglang/pull/41813) keep only TP and PP groups on model runner
- [#41817](https://github.com/sgl-project/sglang/pull/41817) draft TP scopes by attention ownership
- [#41816](https://github.com/sgl-project/sglang/pull/41816) make_pp_layers
- [#41812](https://github.com/sgl-project/sglang/pull/41812) and [#41811](https://github.com/sgl-project/sglang/pull/41811) drop unread placement attributes and values
- [#42478](https://github.com/sgl-project/sglang/pull/42478), [#41779](https://github.com/sgl-project/sglang/pull/41779), [#42311](https://github.com/sgl-project/sglang/pull/42311), [#42477](https://github.com/sgl-project/sglang/pull/42477), [#42309](https://github.com/sgl-project/sglang/pull/42309), [#42307](https://github.com/sgl-project/sglang/pull/42307), [#42308](https://github.com/sgl-project/sglang/pull/42308), [#42304](https://github.com/sgl-project/sglang/pull/42304) decoders built from stage boundaries (Qwen4-exp, Gemma 4, GLM, Llama, Qwen2, ERNIE, Hunyuan V4 and others)
- [#42299](https://github.com/sgl-project/sglang/pull/42299) LoRA kernel reorganization and CODEOWNERS
- [#41453](https://github.com/sgl-project/sglang/pull/41453) HiCache prefetch retirement helper
- [#42362](https://github.com/sgl-project/sglang/pull/42362) supports_prefix_sharing replaces is_chunk_cache/is_tree_cache
- [#42295](https://github.com/sgl-project/sglang/pull/42295) and [#42354](https://github.com/sgl-project/sglang/pull/42354) streaming sessions and Mamba on UnifiedRadixCache

</details>

<details>
<summary>CI, build & deps (9)</summary>

- [#38641](https://github.com/sgl-project/sglang/pull/38641) CUDA PyTorch stack to 2.14
- [#39012](https://github.com/sgl-project/sglang/pull/39012) transformers 5.17.0
- [#40709](https://github.com/sgl-project/sglang/pull/40709) FlashInfer 0.7.0.post1
- [#41625](https://github.com/sgl-project/sglang/pull/41625) maintenance gate via github-script
- [#39788](https://github.com/sgl-project/sglang/pull/39788) PPU CI backend registration
- [#41500](https://github.com/sgl-project/sglang/pull/41500) NPU consistency GT to CANN 9.1.0
- [#36901](https://github.com/sgl-project/sglang/pull/36901) Qwen3.8-Flash-Next-FP8 AMD nightly
- [#41476](https://github.com/sgl-project/sglang/pull/41476) DeepSeek-V4.1-Flash MI35x nightly accuracy test
- [#41689](https://github.com/sgl-project/sglang/pull/41689) diffusion nightly end-to-end methodology

</details>

<details>
<summary>Docs & tests (8)</summary>

- [#41787](https://github.com/sgl-project/sglang/pull/41787) README refresh
- [#41296](https://github.com/sgl-project/sglang/pull/41296) sync LMSYS blog cards
- [#41966](https://github.com/sgl-project/sglang/pull/41966) diffusion docs recommend Docker
- [#42512](https://github.com/sgl-project/sglang/pull/42512) AMD mori io/umbp playground docs
- [#41952](https://github.com/sgl-project/sglang/pull/41952) prune redundant scheduler unit tests
- [#41825](https://github.com/sgl-project/sglang/pull/41825) H3 final MP4 check in-process
- [#42329](https://github.com/sgl-project/sglang/pull/42329) B200 Cirrascale diffusion baselines
- [#41622](https://github.com/sgl-project/sglang/pull/41622) diffusion explicit residency over preload hints

</details>

<details>
<summary>Newly opened (in progress)</summary>

- [#42284](https://github.com/sgl-project/sglang/pull/42284), [#42317](https://github.com/sgl-project/sglang/pull/42317)-[#42343](https://github.com/sgl-project/sglang/pull/42343) LoRA 1-17 stack: dense and MoE execution engines, CuTeDSL/Triton/Marlin providers, tuned tile tables
- [#42381](https://github.com/sgl-project/sglang/pull/42381)-[#42386](https://github.com/sgl-project/sglang/pull/42386), [#42406](https://github.com/sgl-project/sglang/pull/42406), [#42407](https://github.com/sgl-project/sglang/pull/42407), [#42416](https://github.com/sgl-project/sglang/pull/42416), [#42531](https://github.com/sgl-project/sglang/pull/42531), [#42532](https://github.com/sgl-project/sglang/pull/42532) cake_kernels adapter and opt-in route stack (Kimi-K3, Qwen3.5, DSV4, MiniMax-H3)
- [#42286](https://github.com/sgl-project/sglang/pull/42286)-[#42293](https://github.com/sgl-project/sglang/pull/42293) TCPCG retirement refactors (2-9 of 9)
- [#42411](https://github.com/sgl-project/sglang/pull/42411)-[#42414](https://github.com/sgl-project/sglang/pull/42414), [#42507](https://github.com/sgl-project/sglang/pull/42507), [#42509](https://github.com/sgl-project/sglang/pull/42509), [#42513](https://github.com/sgl-project/sglang/pull/42513), [#42514](https://github.com/sgl-project/sglang/pull/42514) PDMux for DeepSeek V4.1 and GLM
- [#41847](https://github.com/sgl-project/sglang/pull/41847) DeepSeek-V4 Pro FP4 Triton Gluon decode MoE on ROCm
- [#42351](https://github.com/sgl-project/sglang/pull/42351) LiteTopK decode top-512 for SM100
- [#42245](https://github.com/sgl-project/sglang/pull/42245) unify mHC state machine
- [#42239](https://github.com/sgl-project/sglang/pull/42239) DiffusionGemma FA4 and CUDA graphs on Blackwell
- [#41949](https://github.com/sgl-project/sglang/pull/41949) UltraQuant 4-bit KV cache on AMD
- [#42449](https://github.com/sgl-project/sglang/pull/42449) and [#42447](https://github.com/sgl-project/sglang/pull/42447) Valkey-backed kv-indexer
- [#42210](https://github.com/sgl-project/sglang/pull/42210) sglang-miles GPU delta decode

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f298bcd1f078582866e2e8769f8f85f46fe7d79cfc1cab46f9c61101dd887fe4 -->
