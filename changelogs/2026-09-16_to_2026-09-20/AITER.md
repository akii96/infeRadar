# AITER: PR digest (2026-09-16 to 2026-09-20)

_71 merged, 96 newly opened - source ROCm/AITER, generated 2026-09-20T23:06:22Z_

## TL;DR
- **DeepSeek (V4) got the most attention (23 labels), then Kimi-K3, GLM-5.x, MiniMax and Qwen3.8.** Merged DSV4 work covers sparse-MLA training and indexer ops, MHC forward/backward, a8w8 block-scale GEMM tunings, and mega-MoE decode on gfx1250.
- **Biggest merged perf and kernel work:** Gluon sparse paged attention and Sparse MLA on gfx950, FlyDSL FP8 MoE kernels for MI308, a gfx950 bf16 OPUS MLA decode path, and a unified OPUS GEMM/BMM interface. A long tail of FlyDSL and HIP fixes covers MoE routing, top-k and quant epilogues.
- **gfx1250 bring-up is the dominant hardware thread (25 labels)** across FlyDSL MoE EP, OPUS/ASM GEMM and MLA, Gluon BF16 GEMM, and a gfx1250 per-group quant kernel.
- **Open pipeline:** GPT-OSS IQ2R 2-bit MoE, OPUS PA decode, fused Qwen3-Next GDN prefill, FP8 and MXFP8 Flash Attention v2, mixed MXFP6/MXFP4 GEMMs, fused all-reduce + RMSNorm, and a Conv3D kernel.
- **Direction:** tuning tables for new model shapes, FlyDSL and Gluon kernels replacing older paths, and a repo reorg (open PRs 4 through 7).

## Most important PRs
**[#4919](https://github.com/ROCm/aiter/pull/4919) Gluon sparse paged attention and Sparse MLA (gfx950)**
This is the sparse attention backbone for DSV4-style sparse-MLA models. It is a 56-commit Triton/Gluon implementation with tests.

**[#3987](https://github.com/ROCm/aiter/pull/3987) FlyDSL FP8 MoE kernels for MI308**
It adds FP8 MoE decode kernels with weight decompression, plus prefill kernels, on gfx942. It targets Qwen3.5-35B/397B and Hunyuan3.

**[#4961](https://github.com/ROCm/aiter/pull/4961) Unified OPUS GEMM/BMM interfaces with Torch workspaces**
It consolidates the OPUS GEMM and batched-GEMM entry points across gfx942/950/1250. Workspaces now come from Torch's allocator, and the change touches 67 files.

**[#5447](https://github.com/ROCm/aiter/pull/5447) gfx1250 TDM dispatch for mega-MoE expert parallelism**
It brings tensor-data-mover dispatch into the FlyDSL mega-MoE EP path. This is the core of the DSV4 gfx1250 MoE work, alongside [#5489](https://github.com/ROCm/aiter/pull/5489) and [#5507](https://github.com/ROCm/aiter/pull/5507).

**[#5651](https://github.com/ROCm/aiter/pull/5651) gfx950 bf16 OPUS MLA decode path**
It adds a bf16 MLA decode kernel path for gfx950 and merges the separate opus decode modules into one.

## More changes by area

<details>
<summary>Performance & tuning (44)</summary>

- [#5631](https://github.com/ROCm/aiter/pull/5631) optimize dynamic_per_group_scaled_quant
- [#5273](https://github.com/ROCm/aiter/pull/5273) gfx1250 per-group quant perf
- [#5582](https://github.com/ROCm/aiter/pull/5582) MLA PS mode BF16 nhead96 speedup
- [#5586](https://github.com/ROCm/aiter/pull/5586) route untuned a8w8 blockscale GEMMs to Triton above a per-arch M
- [#5703](https://github.com/ROCm/aiter/pull/5703) argmax split count passed as an argument instead of a build parameter
- [#5546](https://github.com/ROCm/aiter/pull/5546) pa_decode dynamic KV work planning and partition scheduling
- [#5373](https://github.com/ROCm/aiter/pull/5373) gfx1250 hca_compress optimization
- [#5334](https://github.com/ROCm/aiter/pull/5334) topk_gating E=512 prefill_n softmax dispatch
- [#5632](https://github.com/ROCm/aiter/pull/5632) register-resident grouped topk for single-group MoE
- [#5508](https://github.com/ROCm/aiter/pull/5508) FP8 FMHA split-K for short cached-prefix queries
- [#5489](https://github.com/ROCm/aiter/pull/5489) DSV4 conc2048 decoding mega-MoE optimization (gfx1250)
- [#5507](https://github.com/ROCm/aiter/pull/5507) quantize MoE a1 scale and shuffle (gfx1250)
- [#5412](https://github.com/ROCm/aiter/pull/5412) packed BF16 mHC and gfx1250 tuning
- [#5274](https://github.com/ROCm/aiter/pull/5274) quantize each MoE token once per route (gfx1250); reverted by [#5581](https://github.com/ROCm/aiter/pull/5581)
- [#5581](https://github.com/ROCm/aiter/pull/5581) revert of [#5274](https://github.com/ROCm/aiter/pull/5274)
- [#5602](https://github.com/ROCm/aiter/pull/5602) GLM-5.3 Flash GEMM configs (gfx950)
- [#5353](https://github.com/ROCm/aiter/pull/5353) Kimi-K3 bf16 tuned GEMM CSV update
- [#5350](https://github.com/ROCm/aiter/pull/5350) Qwen3.8-27B MXFP4 configs (gfx950)
- [#5072](https://github.com/ROCm/aiter/pull/5072) GLM-5.2 TP4 a8w8 blockscale GEMM tunings (gfx942)
- [#5440](https://github.com/ROCm/aiter/pull/5440) DSV4 shared-expert large-M tuning (gfx950)
- [#5378](https://github.com/ROCm/aiter/pull/5378) GLM-5.2 native-MTP M=4 projection tuning
- [#5468](https://github.com/ROCm/aiter/pull/5468) Kimi-K3 a8w4 route-out stage2 retune
- [#5613](https://github.com/ROCm/aiter/pull/5613) PA prefill/decode configs for the triton 3.8 regression
- open: [#5628](https://github.com/ROCm/aiter/pull/5628) pa_decode MTP work budgets and planned reduction
- open: [#5652](https://github.com/ROCm/aiter/pull/5652) fold shared-expert gate GEMV into topk_softmax
- open: [#5671](https://github.com/ROCm/aiter/pull/5671) biased_grouped_topk router load batching
- open: [#5700](https://github.com/ROCm/aiter/pull/5700) non-preshuffle MQA logits decode address-math cuts
- open: [#5702](https://github.com/ROCm/aiter/pull/5702) Kimi-K3 BF16 GEMM tuning (FlyDSL)
- open: [#5690](https://github.com/ROCm/aiter/pull/5690) gfx950 A8W8 preshuffle GEMM shape coverage
- open: [#5657](https://github.com/ROCm/aiter/pull/5657) DSV4-Flash GEMM configs (gfx950)
- open: [#5585](https://github.com/ROCm/aiter/pull/5585) Qwen3.8-27B TP1 a8w8 blockscale tunings (gfx942)
- open: [#5691](https://github.com/ROCm/aiter/pull/5691) per-shape GEMM configs for MI308X
- open: [#5610](https://github.com/ROCm/aiter/pull/5610) restore gfx1250 gluon a16w16 tuned configs
- open: [#5688](https://github.com/ROCm/aiter/pull/5688) GLM-5.2 o_proj CK Tile switch at M=1024
- open: [#5701](https://github.com/ROCm/aiter/pull/5701) gfx1250 MoE ep8 tuned config
- open: [#5650](https://github.com/ROCm/aiter/pull/5650) gfx942 Gemma-4 large-prefill attn_2d entries
- open: [#5664](https://github.com/ROCm/aiter/pull/5664) Gemma-4 unified attention configs (MI325)
- open: [#5601](https://github.com/ROCm/aiter/pull/5601) gfx1151 Gemma-4 prefill tuning
- open: [#5669](https://github.com/ROCm/aiter/pull/5669) Qwen3.8 MXFP4 GDN in_proj_ba tiles
- open: [#5621](https://github.com/ROCm/aiter/pull/5621) gfx950 FP8 MQA prefill dispatch tuning
- open: [#5598](https://github.com/ROCm/aiter/pull/5598) unified-attention skip-mask for gfx950 hd256 FP8 prefill
- open: [#5618](https://github.com/ROCm/aiter/pull/5618) DSV4.1 Flash BF16 GEMM tuning
- open: [#5575](https://github.com/ROCm/aiter/pull/5575) DSPARK a8w8 blockscale bpreshuffle configs
- open: [#5682](https://github.com/ROCm/aiter/pull/5682) fp8_mqa_logits split oversubscription raised to 16x CU

</details>

<details>
<summary>Kernels & attention (34)</summary>

- [#5397](https://github.com/ROCm/aiter/pull/5397) OPUS GEMM 256-tile ring
- [#5639](https://github.com/ROCm/aiter/pull/5639) Gluon BF16 GEMM config (gfx1250)
- [#5491](https://github.com/ROCm/aiter/pull/5491) DSV4 sparse-MLA training and indexer ops
- [#5492](https://github.com/ROCm/aiter/pull/5492) MHC forward/backward for DSV4 (Gluon)
- [#5363](https://github.com/ROCm/aiter/pull/5363) FlyDSL radix top-k one-block kernel
- [#5406](https://github.com/ROCm/aiter/pull/5406) a8w8 mxfp8_128 GEMM A-preshuffle and fused split-k (gfx1250)
- [#5217](https://github.com/ROCm/aiter/pull/5217) RDNA3 fp8 enablement and DSV4 A8W8 block-scale configs
- [#5400](https://github.com/ROCm/aiter/pull/5400) FP8 output support in gather_kv_b_proj
- [#5107](https://github.com/ROCm/aiter/pull/5107) OPUS auto-detect stepping and B0-only guard (gfx1250)
- [#5043](https://github.com/ROCm/aiter/pull/5043) gfx1250 asm MHA bf16 hd192x128
- [#5603](https://github.com/ROCm/aiter/pull/5603) split-k for fp8 MQA logits (gfx950)
- [#5580](https://github.com/ROCm/aiter/pull/5580) gfx1250 MLA v4 sparse prefill rebuild
- [#5635](https://github.com/ROCm/aiter/pull/5635) avoid padded CSR tail replay in QH128 prefill
- [#5636](https://github.com/ROCm/aiter/pull/5636) avoid vectorizing the A16W4 upper clamp
- open: [#5640](https://github.com/ROCm/aiter/pull/5640) Triton Conv3D kernels
- open: [#5593](https://github.com/ROCm/aiter/pull/5593) OPUS PA decode (gfx950)
- open: [#5606](https://github.com/ROCm/aiter/pull/5606) fused Qwen3-Next GDN prefill with fp8 group-quant epilogue
- open: [#5578](https://github.com/ROCm/aiter/pull/5578) MXFP8 Flash Attention v2 (gfx950)
- open: [#5577](https://github.com/ROCm/aiter/pull/5577) FP8 Flash Attention v2 (gfx942/950)
- open: [#5656](https://github.com/ROCm/aiter/pull/5656) OPUS PA MQA logits MXFP4 (gfx1250)
- open: [#5677](https://github.com/ROCm/aiter/pull/5677) adaptive decode Top-K kernel (FlyDSL)
- open: [#5626](https://github.com/ROCm/aiter/pull/5626) MiniMax M3 index score kernel (FlyDSL)
- open: [#5637](https://github.com/ROCm/aiter/pull/5637) gfx1250 per-tensor FP8 MHA prefill
- open: [#5592](https://github.com/ROCm/aiter/pull/5592) long-context FMHA split-KV (gfx942)
- open: [#5709](https://github.com/ROCm/aiter/pull/5709) speculative KDA decode for Kimi-K3 (gfx950)
- open: [#5686](https://github.com/ROCm/aiter/pull/5686) per-row top-k (gfx950)
- open: [#5707](https://github.com/ROCm/aiter/pull/5707) 4-wave FP4 MQA prefill (gfx950)
- open: [#5680](https://github.com/ROCm/aiter/pull/5680) DSv4 paged K gather and dequant kernel
- open: [#5699](https://github.com/ROCm/aiter/pull/5699) F8GEMM 256x256 split-K and 128x128 kernels (gfx1250)
- open: [#5695](https://github.com/ROCm/aiter/pull/5695) MLA PS mode nhead12/8 support
- open: [#5623](https://github.com/ROCm/aiter/pull/5623) fused fp8 MQA logits clean
- open: [#5619](https://github.com/ROCm/aiter/pull/5619) order KDA decode conv_state shifts after tap loads
- open: [#5624](https://github.com/ROCm/aiter/pull/5624) strided leading dimensions in GDN L2Norm
- open: [#5672](https://github.com/ROCm/aiter/pull/5672) drop GRID_MN from batched MXFP4 GEMM specialisation keys
- open: [#5668](https://github.com/ROCm/aiter/pull/5668) key MXFP8 BMM tuned lookup on cu_num

</details>

<details>
<summary>MoE & quantization (21)</summary>

- [#5579](https://github.com/ROCm/aiter/pull/5579) gfx950 wideEP MoE test for a8w4 DSV4 and a4w4 Kimi-K3
- [#5439](https://github.com/ROCm/aiter/pull/5439) FP8 MoE intermediate option for Kimi-K3 a4w4
- [#5221](https://github.com/ROCm/aiter/pull/5221) expose fused_moe activation dtype resolution
- [#5660](https://github.com/ROCm/aiter/pull/5660) raise the stage-2 invalid-row sentinel to 4 GiB
- [#5622](https://github.com/ROCm/aiter/pull/5622) bind comm-fused GEMM2 to the sorted-inter layout
- open: [#5678](https://github.com/ROCm/aiter/pull/5678) GPT-OSS IQ2R 2-bit MoE
- open: [#5587](https://github.com/ROCm/aiter/pull/5587) mixed MXFP6/MXFP4 GEMMs
- open: [#5583](https://github.com/ROCm/aiter/pull/5583) MXFP4 weights on gfx942 (a16w4)
- open: [#5704](https://github.com/ROCm/aiter/pull/5704) stage1 fusion for mega-MoE EP (gfx1250)
- open: [#5693](https://github.com/ROCm/aiter/pull/5693) herd_fused_topk selector for fused_moe 2-stage
- open: [#5588](https://github.com/ROCm/aiter/pull/5588) remove g2l for EP and take local_expert_hash as an argument
- open: [#5571](https://github.com/ROCm/aiter/pull/5571) fmoe runcfg gatemode verify
- open: [#5708](https://github.com/ROCm/aiter/pull/5708) relu2 in CK-Tile fused MoE GEMM
- open: [#5689](https://github.com/ROCm/aiter/pull/5689) standalone relu2 elementwise kernel
- open: [#5667](https://github.com/ROCm/aiter/pull/5667) a16w4 MoE tuned dispatch and gfx942 DSv4.1 tables
- open: [#5658](https://github.com/ROCm/aiter/pull/5658) merge MoE MXFP8 GEMM into _moe_gemm_a8w8
- open: [#5625](https://github.com/ROCm/aiter/pull/5625) DSv4 a4w4 fused-MoE tables (gfx950)
- open: [#5609](https://github.com/ROCm/aiter/pull/5609) DSV4.1 Flash TP4 MoE tuning
- open: [#5599](https://github.com/ROCm/aiter/pull/5599) GLM-5.3 routed MoE rows
- open: [#5641](https://github.com/ROCm/aiter/pull/5641) retune DSR1/V3 FP8 fmoe rows
- open: [#5706](https://github.com/ROCm/aiter/pull/5706) DSv4 EP16 a4w4 tables and MXFP4 aux whitelist fix

</details>

<details>
<summary>Parallelism & scheduling (3)</summary>

- open: [#5670](https://github.com/ROCm/aiter/pull/5670) fused all-reduce + RMSNorm (FlyDSL)
- open: [#5616](https://github.com/ROCm/aiter/pull/5616) gfx1250 ll128 cas2shot all-reduce
- open: [#5604](https://github.com/ROCm/aiter/pull/5604) SYSTEM-scope P2P all-reduce flags and split 1-stage start_sync

</details>

<details>
<summary>Bugfixes (28)</summary>

- [#5576](https://github.com/ROCm/aiter/pull/5576) missing block_reduce barrier and indexer_qk_rope_quant_and_cache rewrite
- [#5295](https://github.com/ROCm/aiter/pull/5295) skip invalid expert IDs in MoE sorting
- [#5325](https://github.com/ROCm/aiter/pull/5325) hipBLASLt extension init resource leaks
- [#5629](https://github.com/ROCm/aiter/pull/5629) mha_varlen_with_pe miscompile
- [#5519](https://github.com/ROCm/aiter/pull/5519) FMoE GEMM2 A addressing chosen by stored buffer size
- [#4916](https://github.com/ROCm/aiter/pull/4916) ASM split-K semaphore deadlock under CUDA graph capture
- [#5385](https://github.com/ROCm/aiter/pull/5385) ck_batched_gemm_bf16 operand strides from tensors
- [#5573](https://github.com/ROCm/aiter/pull/5573) pad MXFP4 A4W4 MoE sort extent to a block_size multiple
- [#5175](https://github.com/ROCm/aiter/pull/5175) triton 3.8 rmsnorm regression
- [#5681](https://github.com/ROCm/aiter/pull/5681) tuned_gemm honours otype
- [#5653](https://github.com/ROCm/aiter/pull/5653) grouped-quant shape for the 4096<n<=6144 RMSNorm bucket
- [#5655](https://github.com/ROCm/aiter/pull/5655) MoE aux kernel unit test
- [#5558](https://github.com/ROCm/aiter/pull/5558) MoE routing kernel compile failure
- [#5627](https://github.com/ROCm/aiter/pull/5627) Triton 3.6 FP8 MQA logits gluon kernel
- [#5638](https://github.com/ROCm/aiter/pull/5638) release v0.1.22 cherry-picks (MXFP4 MoE OOB fix and more)
- open: [#5614](https://github.com/ROCm/aiter/pull/5614) non-preshuffle MQA paging and large KV offsets
- open: [#5572](https://github.com/ROCm/aiter/pull/5572) Python 3.10 source inspection in MXFP4 JIT imports
- open: [#5692](https://github.com/ROCm/aiter/pull/5692) PA GQA16 short-tail PS
- open: [#5648](https://github.com/ROCm/aiter/pull/5648) mask the >2GB global_load path in mla_gluon decode
- open: [#5698](https://github.com/ROCm/aiter/pull/5698) lift the 2 GiB limit on mla_reduce_v1 output and LSE
- open: [#5600](https://github.com/ROCm/aiter/pull/5600) two-step addressing in paged MQA logits
- open: [#5630](https://github.com/ROCm/aiter/pull/5630) 64-aligned A16W16 shards in CK dispatch
- open: [#5694](https://github.com/ROCm/aiter/pull/5694) custom_all_reduce uniform barrier trip count
- open: [#5642](https://github.com/ROCm/aiter/pull/5642) scale FP8 softmax probabilities into the e4m3 normal range
- open: [#5675](https://github.com/ROCm/aiter/pull/5675) gfx942 head_size>=512 decode KV over-segmentation
- open: [#5654](https://github.com/ROCm/aiter/pull/5654) gfx950 GQA16 FP8 paged attention short-tail NaNs
- open: [#5591](https://github.com/ROCm/aiter/pull/5591) repro for paged-MQA-logits Preshuffle=False OOB
- open: [#5663](https://github.com/ROCm/aiter/pull/5663) fp8 KV correctness reference in bench_unified_attention

</details>

<details>
<summary>Tests (8)</summary>

- [#5423](https://github.com/ROCm/aiter/pull/5423) route Triton/Gluon test print() through the aiter logger
- [#5590](https://github.com/ROCm/aiter/pull/5590) take autotuning search out of unit tests
- [#5574](https://github.com/ROCm/aiter/pull/5574) benchmark for fused_add_rmsnorm_pad
- [#5424](https://github.com/ROCm/aiter/pull/5424) no CSV under pytest, no leaked default device
- open: [#5608](https://github.com/ROCm/aiter/pull/5608) Norm/Layernorm benchmark
- open: [#5676](https://github.com/ROCm/aiter/pull/5676) fused_rmsnorm_add benchmark
- open: [#5665](https://github.com/ROCm/aiter/pull/5665) sliding_window in bench_unified_attention metrics
- open: [#5647](https://github.com/ROCm/aiter/pull/5647) drop stale use_aot flag from bench_gemm_afp4wfp4

</details>

<details>
<summary>CI & build (18)</summary>

- [#5596](https://github.com/ROCm/aiter/pull/5596) enable 2P1D vLLM DI CI cases and bump to v0.29.0
- [#5620](https://github.com/ROCm/aiter/pull/5620) use PR aiter when installing Flash Attention Triton
- [#5612](https://github.com/ROCm/aiter/pull/5612) bump triton to 7cb7b059
- [#5457](https://github.com/ROCm/aiter/pull/5457) bump flydsl to 0.3.4.1
- [#5697](https://github.com/ROCm/aiter/pull/5697) lower Kimi vLLM GPU memory utilization
- open: [#5666](https://github.com/ROCm/aiter/pull/5666) self-hosted GLM PR reviewer
- open: [#5617](https://github.com/ROCm/aiter/pull/5617) stale branch archive
- open: [#5685](https://github.com/ROCm/aiter/pull/5685) add PRs to the AITER-triton Kernels board without labels
- open: [#5687](https://github.com/ROCm/aiter/pull/5687) Flash Attention CI failures
- open: [#5570](https://github.com/ROCm/aiter/pull/5570) reorg 3 infra
- open: [#5569](https://github.com/ROCm/aiter/pull/5569) reorg 2 import fix
- open: [#5568](https://github.com/ROCm/aiter/pull/5568) recursive aiter test collection
- open: [#5634](https://github.com/ROCm/aiter/pull/5634) MiniMax-M3 MXFP8 2P1D TP8 ATOM DI CI
- open: [#5645](https://github.com/ROCm/aiter/pull/5645) remove stale rocm/vllm-dev:nightly image
- open: [#5584](https://github.com/ROCm/aiter/pull/5584) bump flydsl to 0.3.3.dev903
- open: [#5615](https://github.com/ROCm/aiter/pull/5615) DO NOT MERGE triton bump
- open: [#5659](https://github.com/ROCm/aiter/pull/5659) re-enable contexted kv attention tests
- open: [#5605](https://github.com/ROCm/aiter/pull/5605) prebuild nmask/nlse bf16 mha_varlen_fwd variant

</details>

<details>
<summary>Refactors (4)</summary>

- open: [#5567](https://github.com/ROCm/aiter/pull/5567) aiter reorg 7
- open: [#5566](https://github.com/ROCm/aiter/pull/5566) aiter reorg 6 (MoE fusions)
- open: [#5565](https://github.com/ROCm/aiter/pull/5565) aiter reorg 5 (attention)
- open: [#5564](https://github.com/ROCm/aiter/pull/5564) aiter reorg 4 (GEMM and top-k)

</details>

<details>
<summary>Docs (1)</summary>

- open: [#5597](https://github.com/ROCm/aiter/pull/5597) refresh onboarding docs and enforce source-backed reference checks

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 7af415586f44630652a6c3b7418fed754be21c35246abf06378e971e20abbbc6 -->
