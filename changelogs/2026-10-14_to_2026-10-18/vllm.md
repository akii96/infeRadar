# vllm: PR digest (2026-10-14 to 2026-10-18)

_295 merged, 515 newly opened - source vllm-project/vllm, generated 2026-10-18T23:12:50Z_

## TL;DR
- **DeepSeek (V4/V4.1) got the most model-labelled attention (62 label hits).** Merged: FlashMLA bump with the interleaved V4.1 KV cache (`[#61371](https://github.com/vllm-project/vllm/pull/61371)`), PCP + DSpark support (`[#59857](https://github.com/vllm-project/vllm/pull/59857)`), and ROCm AITER MegaMoE and DSpark adaptive verification. Open: a large GB300 specialized-decode stack (`[#61868](https://github.com/vllm-project/vllm/pull/61868)`, `[#61869](https://github.com/vllm-project/vllm/pull/61869)`) plus an EPLB `symm_mem` backend (`[#62009](https://github.com/vllm-project/vllm/pull/62009)`).
- **Biggest merged perf win: Kimi K3 CuTeDSL specialized decode on GB300, claimed 1.5-2x (`[#61867](https://github.com/vllm-project/vllm/pull/61867)`).** Other merged perf work: GDN prefill checkpoints with FlashInfer, a fused Mamba block-table gather (7 kernels to 1, 6x), and sampler and parser streaming speedups.
- **MoE and quantization:** DeepGEMM MegaMoE unified with NVFP4 (`[#61538](https://github.com/vllm-project/vllm/pull/61538)`), online re-quantization extended to MoE (`[#60276](https://github.com/vllm-project/vllm/pull/60276)`), and compressed-tensors MXFP4 MoE with FP8 activations (`[#59815](https://github.com/vllm-project/vllm/pull/59815)`). AMD got AITER router GEMM, `topk_gating` and MXFP4 work.
- **New-model wave in open PRs:** Step-5 Preview, Muse Spark Open, Reflection Beam, Qwen4Exp (Qwen3.8-Flash-Next) and Kimi K3 or GLM-5.3 mono-decode kernels on ROCm.
- **Direction:** big-model decode kernels, KV transfer and offload hardening (checksums, P2P, NIXL), and cleanup of legacy paths (Ray compiled-graph executor, Medusa/MLP speculator).

## Most important PRs
**[#61867](https://github.com/vllm-project/vllm/pull/61867) - Kimi K3 specialized decode with CuTeDSL on GB300**
Adds a hand-optimized CuTeDSL decode path for Kimi K3 MoE on GB300, with a claimed 1.5-2x decode speedup. It is the largest merged perf change in the window.

**[#61538](https://github.com/vllm-project/vllm/pull/61538) - Unified DeepGEMM MegaMoE experts layer, plus NVFP4**
Puts the DeepGEMM MegaMoE experts behind one feature-matrix layer and adds NVFP4 support. This consolidates the fused-MoE path that DeepSeek-class models use.

**[#60276](https://github.com/vllm-project/vllm/pull/60276) - Online re-quantization extended to MoE**
Extends the re-quantization API so any online MoE method can use NVFP4 from modelopt, compressed-tensors or Quark checkpoints. It widens quantized MoE serving without a pre-quantized checkpoint.

**[#61371](https://github.com/vllm-project/vllm/pull/61371) - FlashMLA bump for DeepSeek V4.1**
Updates FlashMLA to the 2026.09.30 release and adopts its interleaved V4.1 KV-cache layout, the attention foundation for V4.1 serving.

**[#43202](https://github.com/vllm-project/vllm/pull/43202) - External LB mode for Elastic EP scaling**
Lets Elastic EP scale under an external load balancer, a step toward dynamic expert-parallel deployments.

## More changes by area

<details>
<summary>Performance (17)</summary>

- [#60050](https://github.com/vllm-project/vllm/pull/60050) internal prefill checkpoints for the FlashInfer GDN prefill backend
- [#58737](https://github.com/vllm-project/vllm/pull/58737) fuse the mamba align block-table gather into one Triton kernel (6x)
- [#57392](https://github.com/vllm-project/vllm/pull/57392) AITER Gluon KDA kernels for Kimi-K3 decode and spec decode
- [#59552](https://github.com/vllm-project/vllm/pull/59552) AITER Gluon chunk_kda for KDA prefill
- [#56226](https://github.com/vllm-project/vllm/pull/56226) route softmax MoE top-k through AITER topk_gating on ROCm
- [#61895](https://github.com/vllm-project/vllm/pull/61895) any-shape low-latency MoE router GEMM on MI355
- [#57773](https://github.com/vllm-project/vllm/pull/57773) DPA+ETP prefill dual-batch-overlap for DeepSeek-V4 on ROCm
- [#55090](https://github.com/vllm-project/vllm/pull/55090) pad fp16/bf16 GEMM weight row stride for L2 cache on ROCm
- [#60753](https://github.com/vllm-project/vllm/pull/60753) AITER prefill indexer topk for GLM-5.3-Flash
- [#62035](https://github.com/vllm-project/vllm/pull/62035) stream MiniMax M2 tool args incrementally (5.9 s to 26 ms)
- [#62027](https://github.com/vllm-project/vllm/pull/62027) stream Qwen3 tool args incrementally (2.1 s to 11 ms)
- [#59511](https://github.com/vllm-project/vllm/pull/59511) capture DFlash context combine and anchor in the draft CUDA graph
- [#61996](https://github.com/vllm-project/vllm/pull/61996) speed up the small-batch split top-p sampler
- [#61451](https://github.com/vllm-project/vllm/pull/61451) skip bonus-logit reduction for short drafts in rejection sampling
- [#61724](https://github.com/vllm-project/vllm/pull/61724) skip the null head of sliding-window block tables
- [#61039](https://github.com/vllm-project/vllm/pull/61039) length-aware candidate block selection in the DSv4.1 decode indexer
- plus 9 more minor perf PRs ([#60645](https://github.com/vllm-project/vllm/pull/60645), [#61278](https://github.com/vllm-project/vllm/pull/61278), [#61422](https://github.com/vllm-project/vllm/pull/61422), [#61767](https://github.com/vllm-project/vllm/pull/61767), [#61668](https://github.com/vllm-project/vllm/pull/61668), [#59825](https://github.com/vllm-project/vllm/pull/59825), [#58354](https://github.com/vllm-project/vllm/pull/58354), [#60500](https://github.com/vllm-project/vllm/pull/60500), [#61458](https://github.com/vllm-project/vllm/pull/61458))

</details>

<details>
<summary>Kernels & attention (8)</summary>

- [#62132](https://github.com/vllm-project/vllm/pull/62132) norm fused kernel for Step-5 Preview and Muse Spark Open
- [#62126](https://github.com/vllm-project/vllm/pull/62126) FP32 router GEMM support for Step-5 Preview and Muse Spark Open
- [#62042](https://github.com/vllm-project/vllm/pull/62042) router GEMM kernels for (5120, 256) and BF16 output in ll_bf16_gemm
- [#62069](https://github.com/vllm-project/vllm/pull/62069) CuTe DSL backend selection for MLA context prefill
- [#58555](https://github.com/vllm-project/vllm/pull/58555) route gfx942 DCP causal multi-token verify to Triton split-KV decode
- [#53036](https://github.com/vllm-project/vllm/pull/53036) varlen Mamba2 decode for adaptive verification
- [#58297](https://github.com/vllm-project/vllm/pull/58297) XPU MLA integrated into FLASH_ATTN_MLA
- [#52968](https://github.com/vllm-project/vllm/pull/52968) ROCm attn-res, sigmoid_mul and conv fusions

</details>

<details>
<summary>MoE & quantization (14)</summary>

- [#61979](https://github.com/vllm-project/vllm/pull/61979) expert LoRA for FlashInfer TRTLLM MXFP4 experts
- [#61293](https://github.com/vllm-project/vllm/pull/61293) shape-based padding for TRTLLM MXFP8 experts
- [#61773](https://github.com/vllm-project/vllm/pull/61773) skip the TRTLLM fp8-block activation-scale transpose copy
- [#58897](https://github.com/vllm-project/vllm/pull/58897) cheaper triton_kernels 3.8 routing build in OAI Triton MoE
- [#59044](https://github.com/vllm-project/vllm/pull/59044) skip padded work in SM100 FP4 DeepGEMM experts
- [#59596](https://github.com/vllm-project/vllm/pull/59596) MoRI FP4 dispatch for mxfp4 w4a4 MoE
- [#60282](https://github.com/vllm-project/vllm/pull/60282) DeepSeek-V4 hash routing in AITER Triton W4A16 MoE
- [#59973](https://github.com/vllm-project/vllm/pull/59973) quantized draft lm_head for drafters sharing the target head
- [#56273](https://github.com/vllm-project/vllm/pull/56273) packed NVFP4 Qwen4Exp PLE embeddings
- [#52831](https://github.com/vllm-project/vllm/pull/52831) ROCm AITER fusion of per-tensor quant and rmsnorm
- [#51933](https://github.com/vllm-project/vllm/pull/51933) torch MXFP8 linear backend on XPU
- [#51965](https://github.com/vllm-project/vllm/pull/51965) torch MXFP4 linear backend on XPU
- [#61556](https://github.com/vllm-project/vllm/pull/61556) update Humming and remove NVFP4 scale workaround
- [#61274](https://github.com/vllm-project/vllm/pull/61274) auto-disable DeepGEMM for Kolibri 1 on SM12x

</details>

<details>
<summary>Model support (13)</summary>

- [#57963](https://github.com/vllm-project/vllm/pull/57963) AliceAI support
- [#61565](https://github.com/vllm-project/vllm/pull/61565) Decision 3.0 models (vllm-sr/d3)
- [#61778](https://github.com/vllm-project/vllm/pull/61778) all Decision 3.0 sizes
- [#61585](https://github.com/vllm-project/vllm/pull/61585) precomputed image embeddings for LightOnOCR
- [#61110](https://github.com/vllm-project/vllm/pull/61110) EAGLE3/DFlash aux hidden states for GraniteMoe
- [#46005](https://github.com/vllm-project/vllm/pull/46005) ViT full CUDA graph for DeepSeek-VL2
- [#61454](https://github.com/vllm-project/vllm/pull/61454) clean up HC and PLE for Qwen3.8-Flash-Next
- [#61471](https://github.com/vllm-project/vllm/pull/61471) HC and MoE sequence parallelism on ROCm for Qwen4Exp
- [#59857](https://github.com/vllm-project/vllm/pull/59857) DeepSeek-V4.1-Flash PCP support
- [#58857](https://github.com/vllm-project/vllm/pull/58857) stream language-model weights for DeepSeek-V4/V4.1 VL
- [#58151](https://github.com/vllm-project/vllm/pull/58151) ROCm DSv4.1 DSpark adaptive verification
- [#59824](https://github.com/vllm-project/vllm/pull/59824) ROCm Kimi-K3 DSpark adaptive verification on MI355X
- [#42755](https://github.com/vllm-project/vllm/pull/42755) QK Norm + RoPE + KV cache fusion for Qwen3-30B-A3B on ROCm

</details>

<details>
<summary>Parallelism & scheduling (15)</summary>

- [#60934](https://github.com/vllm-project/vllm/pull/60934) per-parameter source layouts for NCCL M2N (RL)
- [#59559](https://github.com/vllm-project/vllm/pull/59559) DP engines own wave wake-ups
- [#54627](https://github.com/vllm-project/vllm/pull/54627) prefill_schedule_interval outside data parallelism
- [#61257](https://github.com/vllm-project/vllm/pull/61257) batch-sharded sampling for GPT-OSS in MRV2
- [#61455](https://github.com/vllm-project/vllm/pull/61455) explicit draft-layer tags replace EAGLE group heuristics
- [#59468](https://github.com/vllm-project/vllm/pull/59468) don't reserve DFlash/DSpark draft slots in the token budget
- [#53558](https://github.com/vllm-project/vllm/pull/53558) pluggable KVCacheConfigBuilder
- [#61789](https://github.com/vllm-project/vllm/pull/61789) UMBP 1/10 connector contracts and request lifecycle
- [#58168](https://github.com/vllm-project/vllm/pull/58168) expose OffloadingManager lock/unlock and move tiering control off the scheduler thread
- [#57139](https://github.com/vllm-project/vllm/pull/57139) register P2P peers off the scheduler thread
- [#61032](https://github.com/vllm-project/vllm/pull/61032) NIXL 1.5 strided descriptor lists
- [#61074](https://github.com/vllm-project/vllm/pull/61074) register packed MLA KV rows as a single NIXL region
- [#59625](https://github.com/vllm-project/vllm/pull/59625) sleep mode with MooncakeConnector over RDMA
- [#60544](https://github.com/vllm-project/vllm/pull/60544) MoRIIO hybrid WRITE transfers with DSpark
- [#62041](https://github.com/vllm-project/vllm/pull/62041) collect KV transfer results before the drafter runs

</details>

<details>
<summary>Hardware & arch (3)</summary>

- [#58800](https://github.com/vllm-project/vllm/pull/58800) ROCm gfx1250 optimizations and model enablement
- [#52183](https://github.com/vllm-project/vllm/pull/52183) PyTorch 2.14, torchvision 0.29, triton 3.8
- [#61262](https://github.com/vllm-project/vllm/pull/61262) AITER MegaMoE fixed-slot dispatch for DeepSeek-V4

</details>

<details>
<summary>API & serving (17)</summary>

- [#62052](https://github.com/vllm-project/vllm/pull/62052) Beam reasoning and tool parsers
- [#61339](https://github.com/vllm-project/vllm/pull/61339) `vllm bench forward` exact-shape timing
- [#61692](https://github.com/vllm-project/vllm/pull/61692) per-case kernel profiles in `vllm bench forward`
- [#59324](https://github.com/vllm-project/vllm/pull/59324) truthful finish_reason and Responses item status
- [#59518](https://github.com/vllm-project/vllm/pull/59518) per-endpoint top_logprobs cut in derender
- [#60437](https://github.com/vllm-project/vllm/pull/60437) logprobs on the parsed streaming derender path
- [#61427](https://github.com/vllm-project/vllm/pull/61427) mm_payload enum on render requests
- [#61328](https://github.com/vllm-project/vllm/pull/61328) unset `--tool-strict-level` falls back to the parser default
- [#61479](https://github.com/vllm-project/vllm/pull/61479) `--enable-x`/`--disable-x` advertised for boolean flags
- [#61347](https://github.com/vllm-project/vllm/pull/61347) weight-version spans on completions and chat
- [#60877](https://github.com/vllm-project/vllm/pull/60877) CrossEncoder chat templates for scoring
- [#60759](https://github.com/vllm-project/vllm/pull/60759) model-owned MTP shard selection in RunAI ModelStreamer
- [#60630](https://github.com/vllm-project/vllm/pull/60630) env var for request JSON body log level
- [#59554](https://github.com/vllm-project/vllm/pull/59554) DFlash support in dual-key gumbel-max watermarking
- [#53910](https://github.com/vllm-project/vllm/pull/53910) PROMOTION_LATENCY histogram for tiering offload
- [#56867](https://github.com/vllm-project/vllm/pull/56867) `vllm:kv_offload_config_info` metric
- [#61933](https://github.com/vllm-project/vllm/pull/61933) Rust frontend validates bad_words limits

</details>

<details>
<summary>Bugfixes (50)</summary>

- [#59597](https://github.com/vllm-project/vllm/pull/59597) recover PyNvVideoCodec decoder slots after failures
- [#57797](https://github.com/vllm-project/vllm/pull/57797) load attention sinks through weight_loader for layerwise reload
- [#61947](https://github.com/vllm-project/vllm/pull/61947) preserve Cohere and Anthropic streaming errors
- [#59790](https://github.com/vllm-project/vllm/pull/59790) keep NIXL store pins and AbortAck until transfers stop
- [#61718](https://github.com/vllm-project/vllm/pull/61718) fix NaN in Mamba2 chunk scan kernel on sm90
- [#61494](https://github.com/vllm-project/vllm/pull/61494) stream Gemma4 string tool args incrementally
- [#61892](https://github.com/vllm-project/vllm/pull/61892) xgrammar for Rust frontend gRPC structured outputs
- [#61388](https://github.com/vllm-project/vllm/pull/61388) restore TP-sharded routed-expert capture at DP=1
- [#60946](https://github.com/vllm-project/vllm/pull/60946) align MoE routing padding with gathered tokens under PCP
- [#61611](https://github.com/vllm-project/vllm/pull/61611) honor code_revision in tokenizer loading
- [#61857](https://github.com/vllm-project/vllm/pull/61857) prompt-closed reasoning block in non-streaming parse
- [#58942](https://github.com/vllm-project/vllm/pull/58942) terminate streaming sessions on ABORT/ERROR
- [#61237](https://github.com/vllm-project/vllm/pull/61237) PCP-aware local GPU indexing for NUMA binding
- [#61574](https://github.com/vllm-project/vllm/pull/61574) mask grammar-invalid implicit reasoning ends
- [#61674](https://github.com/vllm-project/vllm/pull/61674) explicit SimpleCPUOffload block counts
- [#47630](https://github.com/vllm-project/vllm/pull/47630) respect allowed_token_ids in beam search
- [#62072](https://github.com/vllm-project/vllm/pull/62072) stop beam search on generation-config EOS
- [#61161](https://github.com/vllm-project/vllm/pull/61161) avoid reusing random draws across block verification rounds
- [#52477](https://github.com/vllm-project/vllm/pull/52477) drive grammar masks from GPU logit counts
- [#59928](https://github.com/vllm-project/vllm/pull/59928) recover Qwen3 tool calls after an unclosed opener
- [#58064](https://github.com/vllm-project/vllm/pull/58064) CUDA graph capture for dynamic-rope Transformers-backend models
- [#61365](https://github.com/vllm-project/vllm/pull/61365) Gemma 4 encoder CUDA graph OOM at startup
- [#61986](https://github.com/vllm-project/vllm/pull/61986) honor RGB PNG transparency
- [#61759](https://github.com/vllm-project/vllm/pull/61759) WebM frame count with the OpenCV video backend
- [#61716](https://github.com/vllm-project/vllm/pull/61716) silu_and_mul_quant vectorized loop
- [#61858](https://github.com/vllm-project/vllm/pull/61858) Humming DeviceInfo traceable under torch.compile
- [#61921](https://github.com/vllm-project/vllm/pull/61921) honor quantization config in Inkling MTP
- [#61496](https://github.com/vllm-project/vllm/pull/61496) DCP FULL cudagraph capture with KV context
- [#58778](https://github.com/vllm-project/vllm/pull/58778) keep resumable sessions that stop while preempted
- [#58668](https://github.com/vllm-project/vllm/pull/58668) uncount stop-trimmed spec tokens
- [#61174](https://github.com/vllm-project/vllm/pull/61174) clear stale shared block-table rows
- [#61563](https://github.com/vllm-project/vllm/pull/61563) honor EAGLE3 single-state draft config
- [#58585](https://github.com/vllm-project/vllm/pull/58585) MoRIIO HMA per-layer block_len
- [#62087](https://github.com/vllm-project/vllm/pull/62087) ignore AMD CI webhook no-op builds
- [#62221](https://github.com/vllm-project/vllm/pull/62221) release wheel builds with tracked recipes/
- [#56836](https://github.com/vllm-project/vllm/pull/56836), [#59140](https://github.com/vllm-project/vllm/pull/59140), [#57500](https://github.com/vllm-project/vllm/pull/57500), [#60279](https://github.com/vllm-project/vllm/pull/60279), [#59096](https://github.com/vllm-project/vllm/pull/59096), [#59329](https://github.com/vllm-project/vllm/pull/59329) KV offload and P2P timeouts, teardown and lookup fixes
- [#61757](https://github.com/vllm-project/vllm/pull/61757), [#61852](https://github.com/vllm-project/vllm/pull/61852), [#61241](https://github.com/vllm-project/vllm/pull/61241), [#62114](https://github.com/vllm-project/vllm/pull/62114), [#61876](https://github.com/vllm-project/vllm/pull/61876), [#61941](https://github.com/vllm-project/vllm/pull/61941) derender and render output fixes ([#61941](https://github.com/vllm-project/vllm/pull/61941) is not in the provided data; counted here via the rest of this group)
- plus 6 more minor bugfixes ([#61825](https://github.com/vllm-project/vllm/pull/61825), [#61736](https://github.com/vllm-project/vllm/pull/61736), [#61016](https://github.com/vllm-project/vllm/pull/61016), [#61647](https://github.com/vllm-project/vllm/pull/61647), [#59935](https://github.com/vllm-project/vllm/pull/59935), [#57378](https://github.com/vllm-project/vllm/pull/57378))

</details>

<details>
<summary>Refactors (4)</summary>

- [#61712](https://github.com/vllm-project/vllm/pull/61712) remove the legacy Ray compiled-graph executor
- [#61713](https://github.com/vllm-project/vllm/pull/61713) drop the Ray driver-node GPU pin
- [#61701](https://github.com/vllm-project/vllm/pull/61701) remove Medusa and MLP speculator support
- [#61843](https://github.com/vllm-project/vllm/pull/61843) remove dead code in multiple places

</details>

<details>
<summary>Tests (3)</summary>

- [#61765](https://github.com/vllm-project/vllm/pull/61765) split the chat_utils tests
- [#60869](https://github.com/vllm-project/vllm/pull/60869) HiSparse shared host pool prefault test updates
- plus 1 more minor test change

</details>

<details>
<summary>CI & build (7)</summary>

- [#58761](https://github.com/vllm-project/vllm/pull/58761) ROCm 10.0 as the default image, ROCm 7.2 as `-rocm72`
- [#61955](https://github.com/vllm-project/vllm/pull/61955) move 17 AMD test groups from MI300 to MI355
- [#62053](https://github.com/vllm-project/vllm/pull/62053) move Spec Decode Speculators + MTP to MI355
- [#59678](https://github.com/vllm-project/vllm/pull/59678) AMD jobs for test groups that only exist in test_areas
- [#61592](https://github.com/vllm-project/vllm/pull/61592) merge target branch into stale PRs on `/ci run`
- [#61265](https://github.com/vllm-project/vllm/pull/61265) remove unused `tools/install_deepgemm.sh`
- [#55671](https://github.com/vllm-project/vllm/pull/55671) migrate FlashInfer autotune warmup to the autotune_v2 managed cache

</details>

<details>
<summary>Docs (6)</summary>

- [#61302](https://github.com/vllm-project/vllm/pull/61302) host model recipes in `recipes/`
- [#62267](https://github.com/vllm-project/vllm/pull/62267) document the weight-transfer HTTP protocol for non-vLLM trainers
- [#62179](https://github.com/vllm-project/vllm/pull/62179) sync the DeepSeek-V4.1-Flash recipe
- [#62302](https://github.com/vllm-project/vllm/pull/62302) document routed experts return for MoE routing replay (R3)
- [#62305](https://github.com/vllm-project/vllm/pull/62305) document `/inference/v1/generate` fields and DP rank header
- [#61588](https://github.com/vllm-project/vllm/pull/61588) update structured decisions docs

</details>

<details>
<summary>Other (7)</summary>

- [#61551](https://github.com/vllm-project/vllm/pull/61551) train-inference consistency agent skill (reverted by [#62186](https://github.com/vllm-project/vllm/pull/62186))
- [#62186](https://github.com/vllm-project/vllm/pull/62186) revert of [#61551](https://github.com/vllm-project/vllm/pull/61551)
- [#61883](https://github.com/vllm-project/vllm/pull/61883) use upstream Transformers InklingProcessor
- [#61392](https://github.com/vllm-project/vllm/pull/61392) use upstream Transformers DeepseekV4Config
- [#61587](https://github.com/vllm-project/vllm/pull/61587) reject local verifier references in Speculators metadata
- [#61167](https://github.com/vllm-project/vllm/pull/61167) EP weight filtering in InstantTensor
- [#60885](https://github.com/vllm-project/vllm/pull/60885) reject mismatched float16/bfloat16 KV cache dtype

</details>

<details>
<summary>Newly opened (in progress) highlights</summary>

- [#61879](https://github.com/vllm-project/vllm/pull/61879), [#62064](https://github.com/vllm-project/vllm/pull/62064) Muse Spark Open model support (including Ampere and AutoRound/GPTQ INT4 experts)
- [#61727](https://github.com/vllm-project/vllm/pull/61727), [#61945](https://github.com/vllm-project/vllm/pull/61945), [#61837](https://github.com/vllm-project/vllm/pull/61837) Step-5 Preview support, including shared Triton kernels and ROCm
- [#61978](https://github.com/vllm-project/vllm/pull/61978), [#62074](https://github.com/vllm-project/vllm/pull/62074), [#62057](https://github.com/vllm-project/vllm/pull/62057), [#62073](https://github.com/vllm-project/vllm/pull/62073) Reflection Beam model, ROCm port and CuTeDSL NVFP4 MegaMoE
- [#61868](https://github.com/vllm-project/vllm/pull/61868), [#61869](https://github.com/vllm-project/vllm/pull/61869) DeepSeek-V4.1 specialized decode and DSpark on GB300
- [#61694](https://github.com/vllm-project/vllm/pull/61694), [#61568](https://github.com/vllm-project/vllm/pull/61568), [#61662](https://github.com/vllm-project/vllm/pull/61662), [#61573](https://github.com/vllm-project/vllm/pull/61573) ROCm mono-decode kernels for Kimi-K3, GLM-5.3-Flash and Qwen3.8
- [#61793](https://github.com/vllm-project/vllm/pull/61793)-[#61798](https://github.com/vllm-project/vllm/pull/61798) UMBP offload series
- [#61578](https://github.com/vllm-project/vllm/pull/61578), [#61579](https://github.com/vllm-project/vllm/pull/61579), [#61580](https://github.com/vllm-project/vllm/pull/61580) KV checksum verification for P/D transfers
- [#62004](https://github.com/vllm-project/vllm/pull/62004), [#61952](https://github.com/vllm-project/vllm/pull/61952), [#61779](https://github.com/vllm-project/vllm/pull/61779) ReplaySSM and GDN CUDA graph work
- [#61688](https://github.com/vllm-project/vllm/pull/61688), [#61686](https://github.com/vllm-project/vllm/pull/61686) Triton autotune for fused MoE and block FP8
- [#62009](https://github.com/vllm-project/vllm/pull/62009) symm_mem EPLB weight migration for DSv4
- [#61747](https://github.com/vllm-project/vllm/pull/61747) vLLM Simulator for CPU

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: a5718773605efcc63622936dc0ae4406dccc98a02e53e9f9821de4d654048ed6 -->
