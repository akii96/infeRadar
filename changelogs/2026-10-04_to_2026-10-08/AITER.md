# AITER: PR digest (2026-10-04 to 2026-10-08)

_59 merged, 103 newly opened - source ROCm/AITER, generated 2026-10-08T16:11:54Z_

## TL;DR
- **Kimi-K3 and DeepSeek (V4.1 / R1) got the most attention**, followed by GLM-5 and Qwen3.8. Kimi work covers KDA decode, GEMM and MoE tuning. DeepSeek work covers MegaMoE, A8W4 fused MoE and DSR1 GEMM tuning.
- **The biggest merged perf work is on gfx950 attention.** It includes a fused Qwen3-Next GDN decode op, a speculative KDA decode optimization, sparse MLA optimizations, an MLA v4 persistent decode kernel, and a single-launch FlyDSL Mega-mHC.
- **MoE and quantization are the main in-flight themes.** Open PRs add fused route-sort plus activation quant, FlyDSL MoE buffer reuse, MXFP4 MoE tiles, a gfx942 a8w4 stage1 kernel, and a gfx1250 A4W4 prefill path.
- **gfx1250 and gfx942 are getting first-class kernels.** The gfx1250 additions are Gluon MXFP4/MXFP8 quant, multicast, and an LDS-pipelined MLA. gfx942 gets sparse MLA with fp8 KV and an asm MXFP8-weight GEMM.
- Direction: per-model tuning tables and fused decode "mono-kernels" on gfx950, plus a broader hardware and Windows/JIT footprint.

## Most important PRs
**[#6179](https://github.com/ROCm/aiter/pull/6179) [FlyDSL] Single-launch Mega-mHC on gfx950** (merged). Adds a single-launch mHC kernel, 3.2k lines of new code, to cut launch and intermediate overhead.

**[#5709](https://github.com/ROCm/aiter/pull/5709) Speculative KDA decode for Kimi-K3 on gfx950** (merged). Optimizes the speculative-decode KDA path in Triton/Gluon and adds CI coverage for it.

**[#6159](https://github.com/ROCm/aiter/pull/6159) GFX950 sparse MLA optimizations** (merged). Adds 33 commits of Gluon sparse-MLA tuning for the DeepSeek-style sparse attention path.

**[#6126](https://github.com/ROCm/aiter/pull/6126) MLA v4 persistent decode kernel** (merged). Splits the plan helper from an ASM/HIP persistent decode kernel that does the split and merge in-kernel, removing separate reduce work.

**[#6154](https://github.com/ROCm/aiter/pull/6154) / [#6173](https://github.com/ROCm/aiter/pull/6173) / [#6206](https://github.com/ROCm/aiter/pull/6206) (newly opened)**. These are DeepSeek V4.1 Flash full-expert MegaMoE tuning (13k lines), a GLM-5 fused decode-layer MonoKernel, and a fused Kimi-K3 KDA decode with FP8 f_b projection. Together they show the push toward fused, whole-layer decode kernels.

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#5481](https://github.com/ROCm/aiter/pull/5481) splits mla_reduce launcher JIT instantiation across TUs, 121.6s to 7.7s
- [#5987](https://github.com/ROCm/aiter/pull/5987) routes gfx950 large-expert decode to multi-phase MoE sorting
- [#6163](https://github.com/ROCm/aiter/pull/6163) initializes the multi-GPU test process group once instead of per case
- [#6210](https://github.com/ROCm/aiter/pull/6210) reuses FlyDSL MoE intermediate buffers per device, stream and shape (open)
- [#6205](https://github.com/ROCm/aiter/pull/6205) reuses GEMM outputs and tuned A8W8 configs above the largest tuned M (open)
- [#6213](https://github.com/ROCm/aiter/pull/6213) skips the unused valid-split fill for single-split MLA decode (open)
- [#6214](https://github.com/ROCm/aiter/pull/6214) keeps the qlen-eight MLA split floor at batch three (open)
- [#6266](https://github.com/ROCm/aiter/pull/6266) adds MLA single-split fill skip and FP8 descales for varlen FMHA (open)
- [#6236](https://github.com/ROCm/aiter/pull/6236) adds TP2 quick all-reduce through a passive xGMI relay (open)
- [#6270](https://github.com/ROCm/aiter/pull/6270) fuses residual add and row-selective RMSNorm in custom allreduce (open)
- [#6211](https://github.com/ROCm/aiter/pull/6211) fuses residual all-reduce with selective RMSNorm rows (open)
- [#6175](https://github.com/ROCm/aiter/pull/6175) improves HSTU backward performance (open)
- [#6177](https://github.com/ROCm/aiter/pull/6177) speeds up FlashKDA and token-parallel intra forward on gfx950 (open)
- [#6162](https://github.com/ROCm/aiter/pull/6162) tunes GLM-5.3 packed-BF16 mHC post/pre on gfx950 (open)

</details>

<details>
<summary>Kernels & attention (24)</summary>

- [#5520](https://github.com/ROCm/aiter/pull/5520) adds a fused Qwen3-Next GDN decode op for gfx950
- [#6098](https://github.com/ROCm/aiter/pull/6098) adds an LDS-pipelined MLA variant for gfx1250
- [#6145](https://github.com/ROCm/aiter/pull/6145) adds row-group FP4 paged MQA logits for 8- and 64-row pages
- [#5721](https://github.com/ROCm/aiter/pull/5721) enables sparse_mla_fwd on gfx942
- [#5859](https://github.com/ROCm/aiter/pull/5859) makes PA decode v1/v2 dispatch config-driven
- [#3698](https://github.com/ROCm/aiter/pull/3698) masks V load and output store by value head size in unified_attention
- [#6040](https://github.com/ROCm/aiter/pull/6040) makes get_ps_metadata_v1 transfers stream-ordered
- [#6140](https://github.com/ROCm/aiter/pull/6140) adds aiter.paged_mqa_logits with a tuned Gluon/FlyDSL table (open)
- [#6185](https://github.com/ROCm/aiter/pull/6185) adds aiter.mqa_logits with a tuned Triton/FlyDSL table (open)
- [#6153](https://github.com/ROCm/aiter/pull/6153) reads (B, next_n) context lengths in paged MQA logits kernels (open)
- [#6164](https://github.com/ROCm/aiter/pull/6164) stages KV through LDS in fp8_mqa_logits on gfx942 (open)
- [#6133](https://github.com/ROCm/aiter/pull/6133) adds gfx1250 QH128 page1/page64 MLA decode (open)
- [#6132](https://github.com/ROCm/aiter/pull/6132) adds an asm MLA non-persistent fp8 gqa64 qlen1 kernel (open)
- [#6220](https://github.com/ROCm/aiter/pull/6220) adds a gfx942 BF16 MLA persistent decode asm kernel with LSE output (open)
- [#6199](https://github.com/ROCm/aiter/pull/6199) supports fp8 KV caches and fp8 dots in sparse_mla_fwd on gfx942 (open)
- [#6155](https://github.com/ROCm/aiter/pull/6155) adds multimodal prefix support to unified attention (do not merge, open)
- [#6244](https://github.com/ROCm/aiter/pull/6244) allows query_length > 4 on the Gluon PA decode single-KV-head PS path (open)
- [#6241](https://github.com/ROCm/aiter/pull/6241) adds an improved fused KV cache kernel for DSR1 (open)
- [#6226](https://github.com/ROCm/aiter/pull/6226) adds Gluon mhc_fused_post_pre for GFX12 (open)
- [#6168](https://github.com/ROCm/aiter/pull/6168) adds mhc_delayed_gates from split-K partials (open)
- [#6171](https://github.com/ROCm/aiter/pull/6171) adds delayed mHC seam for gfx942 (open)
- [#6169](https://github.com/ROCm/aiter/pull/6169) dispatches LayerNorm ops to Triton when ENABLE_CK=0 (open)
- [#6212](https://github.com/ROCm/aiter/pull/6212) supports sigmoid-gated RMSNorm with per-token FP8 quant (open)
- [#6265](https://github.com/ROCm/aiter/pull/6265) adds a sigmoid gate to per-token FP8 quant in gated RMSNorm (open)

</details>

<details>
<summary>MoE & quantization (28)</summary>

- [#4383](https://github.com/ROCm/aiter/pull/4383) adds Gluon MXFP4/MXFP8 quant for gfx950
- [#4894](https://github.com/ROCm/aiter/pull/4894) adds Gluon MXFP4/MXFP8 quant for gfx1250
- [#5812](https://github.com/ROCm/aiter/pull/5812) adds a scatter epilog to layout-v2 GEMM2
- [#6127](https://github.com/ROCm/aiter/pull/6127) optimizes MegaMoEV2 decode/prefill and fixes a Stage1 LDS broadcast race
- [#6106](https://github.com/ROCm/aiter/pull/6106) adds per-token scale to the a8w8 moe gemm
- [#6118](https://github.com/ROCm/aiter/pull/6118) adds multicast support to gfx1250 MXFP4
- [#6144](https://github.com/ROCm/aiter/pull/6144) speeds up gfx942 a16w4 MXFP4 unpack via fp8 lookup and hardware convert
- [#6078](https://github.com/ROCm/aiter/pull/6078) uses gfx1250 320KB LDS for large-D SiTUv2 quant
- [#6035](https://github.com/ROCm/aiter/pull/6035) removes bad moe gemm wrapper code
- [#6142](https://github.com/ROCm/aiter/pull/6142) reverts relu2 support in CK-Tile fused MoE GEMM
- [#6231](https://github.com/ROCm/aiter/pull/6231) fuses TDM loads explicitly in gfx1250 MXFP4 preshuffle GEMM
- [#5927](https://github.com/ROCm/aiter/pull/5927) makes scaleM_pad a runtime argument in act_mul + MXFP4 quant kernels
- [#6136](https://github.com/ROCm/aiter/pull/6136) optimizes gfx1250 A4W4 MoE prefill with fused GEMM1 quant (open)
- [#6165](https://github.com/ROCm/aiter/pull/6165) adds fused route-sort plus MXFP4 activation quant (open)
- [#6208](https://github.com/ROCm/aiter/pull/6208) fuses Kimi-K3 MoE route sorting and activation quant (open)
- [#6263](https://github.com/ROCm/aiter/pull/6263) fuses route sort and MXFP8 quant for small-M a8w4 (open)
- [#6209](https://github.com/ROCm/aiter/pull/6209) supports Kimi-K3 MXFP4 MoE tiles, strided inputs and SiTUv2 (open)
- [#6264](https://github.com/ROCm/aiter/pull/6264) adds non-256-aligned inter_dim and opt-in stage scratch reuse for MXFP4 MoE (open)
- [#6268](https://github.com/ROCm/aiter/pull/6268) balances MegaMoE v2 prefill with MoonEP (open)
- [#6269](https://github.com/ROCm/aiter/pull/6269) adds FlyDSL MoE v1 work for gfx1250 (open)
- [#6247](https://github.com/ROCm/aiter/pull/6247) adds a gfx942 a8w4 MoE stage1 fp8 kernel (open)
- [#6219](https://github.com/ROCm/aiter/pull/6219) adds fnuz FP8 and MXFP8 moe_gemm_a8w8 on gfx942 (open)
- [#6131](https://github.com/ROCm/aiter/pull/6131) specializes gfx1250 sigmoid top-k family (open)
- [#6272](https://github.com/ROCm/aiter/pull/6272) updates the MegaMoE mori path with zero-copy combine input (open)
- [#6218](https://github.com/ROCm/aiter/pull/6218) adds a FlyDSL A4W4 decode GEMM for M<=16 on gfx950 (open)
- [#6172](https://github.com/ROCm/aiter/pull/6172) adds a gfx942 asm GEMM with BF16 activations and MXFP8 weights (open)
- [#6191](https://github.com/ROCm/aiter/pull/6191) adds Mxfp8 w_scale 1*32 (open)
- [#6258](https://github.com/ROCm/aiter/pull/6258) uses FP32 partials for gfx1250 A8W8 split-K GEMMs (open)

</details>

<details>
<summary>Model support & tuning configs (35)</summary>

- [#5867](https://github.com/ROCm/aiter/pull/5867) DSR1 GEMM tuning
- [#6157](https://github.com/ROCm/aiter/pull/6157) DSR1 tuning, Oct 4
- [#6039](https://github.com/ROCm/aiter/pull/6039) gfx950 preshuffled AFP4WFP4 GEMM configs for Qwen3.8-Flash-Next GDN
- [#5669](https://github.com/ROCm/aiter/pull/5669) Qwen3.8-27B MXFP4 GDN in_proj_ba tiles
- [#5922](https://github.com/ROCm/aiter/pull/5922) Inkling model GEMM configs
- [#6019](https://github.com/ROCm/aiter/pull/6019) Kimi-K3 bf16 tp8 GEMM tuning
- [#6174](https://github.com/ROCm/aiter/pull/6174) DeepSeek-V4.1-Flash TP4 bf16 GEMMs
- [#6125](https://github.com/ROCm/aiter/pull/6125) gfx950 A8W4 fused_moe configs for DSv4.1
- [#5967](https://github.com/ROCm/aiter/pull/5967) dsv41 MoE tuning configs
- [#5986](https://github.com/ROCm/aiter/pull/5986) GLM-5 MXFP4 EP4 decode fused-MoE rows
- [#6227](https://github.com/ROCm/aiter/pull/6227) Kimi-K3 ptpc bpreshuffle GEMM for KDA in_proj
- [#6224](https://github.com/ROCm/aiter/pull/6224) Kimi K3 KDA in_proj bf16 GEMM tuning
- [#5964](https://github.com/ROCm/aiter/pull/5964) fixes docs and removes Kpack from 1250 configs
- [#6117](https://github.com/ROCm/aiter/pull/6117) GFX12 MoE tune
- [#6154](https://github.com/ROCm/aiter/pull/6154) DeepSeek V4.1 Flash MegaMoE full-expert tuning (open)
- [#6259](https://github.com/ROCm/aiter/pull/6259) megamoe tune for Kimi-K3 (open)
- [#6262](https://github.com/ROCm/aiter/pull/6262) Kimi-K3 GEMM tuning with caller-owned outputs (open)
- [#6217](https://github.com/ROCm/aiter/pull/6217) Kimi-K3 BF16 and shared-expert FP4 GEMM tuning (open)
- [#6271](https://github.com/ROCm/aiter/pull/6271) gfx942 Kimi-K3 a16wi4 MoE configs for topk=16 (open)
- [#6235](https://github.com/ROCm/aiter/pull/6235) MiniMax-M3 BF16 GEMM table and ViT projections (open)
- [#6201](https://github.com/ROCm/aiter/pull/6201) Qwen3.8-Flash-Next bf16 GEMM configs (open)
- [#6156](https://github.com/ROCm/aiter/pull/6156) Qwen3.8-27B bf16 GEMM tunings (open)
- [#6143](https://github.com/ROCm/aiter/pull/6143) MiMo-V2.6 unified-attention decode tuning (open)
- [#6190](https://github.com/ROCm/aiter/pull/6190) DSV3 fused-shared-expert fmoe retune on gfx942 (open)
- [#6130](https://github.com/ROCm/aiter/pull/6130) gfx1250 FlashKDA K2 schedule (open)
- [#6240](https://github.com/ROCm/aiter/pull/6240) TDM store in bf16 BMM and DSR1 shape tuning (open)
- [#6234](https://github.com/ROCm/aiter/pull/6234) gfx1250 batched a16w16 for MLA-absorb shapes (open)
- [#6238](https://github.com/ROCm/aiter/pull/6238) gfx1250 batched fp8 output and MLA-absorb tiles (open)
- [#6254](https://github.com/ROCm/aiter/pull/6254) gfx1250 M=1536 DSR1 fused_qkv_a bucket (open)
- [#6158](https://github.com/ROCm/aiter/pull/6158) MoE and MLA configs for gfx1101/1150/1151 (open)
- [#6245](https://github.com/ROCm/aiter/pull/6245) gfx1201 A8W8 GEMM tunings (open)
- [#6256](https://github.com/ROCm/aiter/pull/6256) gfx950 MXFP GEMMs for Wan shapes (open)
- [#6167](https://github.com/ROCm/aiter/pull/6167) per-arch config for sparse_mla (open)
- [#6161](https://github.com/ROCm/aiter/pull/6161) adds x_EQ_x config matcher to unified attention (open)
- [#6206](https://github.com/ROCm/aiter/pull/6206) fused Kimi-K3 KDA decode (open; see above)
- [#6225](https://github.com/ROCm/aiter/pull/6225) moves the a4w4 aux-sort crossover to 1.33 rows per expert (open)

</details>

<details>
<summary>Hardware & arch (6)</summary>

- [#2699](https://github.com/ROCm/aiter/pull/2699) adds Windows JIT support
- [#6273](https://github.com/ROCm/aiter/pull/6273) exports ctypes entry points on Windows and adds a JIT smoke test (open)
- [#6267](https://github.com/ROCm/aiter/pull/6267) adds an optional RDNA3 FlyDSL A8W8 backend (open)
- [#6257](https://github.com/ROCm/aiter/pull/6257) optimizes biased grouped topk on gfx1250 (open)
- [#6253](https://github.com/ROCm/aiter/pull/6253) enables gfx1250 sampling under cpp_itfs (open)
- [#6252](https://github.com/ROCm/aiter/pull/6252) moves FlyDSL to the new TDM interface (open)

</details>

<details>
<summary>Bugfixes (22)</summary>

- [#5915](https://github.com/ROCm/aiter/pull/5915) fixes the Gluon PA decode causal mask across splits
- [#5909](https://github.com/ROCm/aiter/pull/5909) fixes a Gluon PA decode VGPR blow-up on Triton 3.8
- [#5600](https://github.com/ROCm/aiter/pull/5600) hardens paged MQA logits prefetch masks
- [#6092](https://github.com/ROCm/aiter/pull/6092) fixes Conv2D/Conv3D caching for inference tensor weights
- [#5191](https://github.com/ROCm/aiter/pull/5191) drops the unused out_idx workspace in topk_renorm_from_probs
- [#6041](https://github.com/ROCm/aiter/pull/6041) honors padding_value in the HSTU reference helper
- [#6181](https://github.com/ROCm/aiter/pull/6181) fixes the MXFP4/MXFP8 fallback for older Triton
- [#6096](https://github.com/ROCm/aiter/pull/6096) masks inp2 columns with N2 in fused_reduce_rms_fp8_group_quant
- [#6129](https://github.com/ROCm/aiter/pull/6129) allocates custom_all_reduce IPC handle tensors on the host
- [#6166](https://github.com/ROCm/aiter/pull/6166) fixes indexer_k_quant_and_cache launching an undefined wave32 kernel
- [#6071](https://github.com/ROCm/aiter/pull/6071) fixes MoE bench scripts
- [#6139](https://github.com/ROCm/aiter/pull/6139) scales gfx942 v3 FP8 FMHA probabilities before conversion (open)
- [#6138](https://github.com/ROCm/aiter/pull/6138) scales gfx942 Sage probabilities before FP8 conversion (open)
- [#6223](https://github.com/ROCm/aiter/pull/6223) fixes gfx942 BF16 MLA KV addressing beyond 4 GiB (open)
- [#6188](https://github.com/ROCm/aiter/pull/6188) fixes an out-of-bounds read in the MLA metadata planner (open)
- [#6198](https://github.com/ROCm/aiter/pull/6198) rejects non-576-wide MLA rows in mla_decode_stage1_asm_fwd (open)
- [#6170](https://github.com/ROCm/aiter/pull/6170) fixes an async stage-1 LDS pipeline race (open)
- [#6184](https://github.com/ROCm/aiter/pull/6184) avoids the inline-sort MXFP4 path when inter_dim % 256 != 0 (open)
- [#6180](https://github.com/ROCm/aiter/pull/6180) writes -inf LSE for fully masked MHA rows (open)
- [#6215](https://github.com/ROCm/aiter/pull/6215) guards fused MLA query RoPE (open)
- [#6261](https://github.com/ROCm/aiter/pull/6261) sanitizes padded query positions in fused_qk_rope_cat_and_cache_mla (open)
- [#6197](https://github.com/ROCm/aiter/pull/6197) fixes arch_info import without a GPU (open)

</details>

<details>
<summary>Tests (4)</summary>

- [#4444](https://github.com/ROCm/aiter/pull/4444) adds SDXL 1.0 conv2d shapes to conv_shapes.json
- [#6073](https://github.com/ROCm/aiter/pull/6073) removes bench_gemm_afp4wfp4_pre_quant_atomic
- [#6237](https://github.com/ROCm/aiter/pull/6237) surfaces op_test failures that CI silently passes (open)
- [#6251](https://github.com/ROCm/aiter/pull/6251) passes the output buffer in bench_mla (open)
- plus 1 more: [#6186](https://github.com/ROCm/aiter/pull/6186) adds an intel kernel test (open)

</details>

<details>
<summary>CI & build (18)</summary>

- [#6246](https://github.com/ROCm/aiter/pull/6246) reduces split test timing update conflicts
- [#5617](https://github.com/ROCm/aiter/pull/5617) adds a stale branch archive
- [#6182](https://github.com/ROCm/aiter/pull/6182) runs full AITER releases weekly
- [#5540](https://github.com/ROCm/aiter/pull/5540) adds a stale pull request label
- [#6243](https://github.com/ROCm/aiter/pull/6243) uses the ci:multi-gpu label in the welcome comment
- [#6248](https://github.com/ROCm/aiter/pull/6248) adds a topk select tuner (WIP, open)
- [#6242](https://github.com/ROCm/aiter/pull/6242) probes Windows Navi GPU runners (open)
- [#6141](https://github.com/ROCm/aiter/pull/6141) runs pytest regressions in standard shards and discovers FlyDSL tests (open)
- [#6202](https://github.com/ROCm/aiter/pull/6202) adds get_GEMM_A16W16_tuned_config returning None when no row exists (open)
- [#6195](https://github.com/ROCm/aiter/pull/6195) changes the stale PR workflow schedule (open)
- [#6260](https://github.com/ROCm/aiter/pull/6260) fixes metadata-only setup.py, empty rocminfo and torch.Stream handling (open)
- [#6204](https://github.com/ROCm/aiter/pull/6204) uses live HIP device properties when rocminfo is empty (open)
- [#6207](https://github.com/ROCm/aiter/pull/6207) accepts generic torch.Stream in native launch conversion (open)
- [#6203](https://github.com/ROCm/aiter/pull/6203) skips kernel prebuild during package metadata generation (open)
- [#6178](https://github.com/ROCm/aiter/pull/6178) repins the CK submodule to a fetchable develop commit (open)
- [#6183](https://github.com/ROCm/aiter/pull/6183) opts attention kernels into FP fusion explicitly (open)
- [#6216](https://github.com/ROCm/aiter/pull/6216) passes per-tensor q/k/v descales to FlyDSL varlen attention (open)
- [#6250](https://github.com/ROCm/aiter/pull/6250) uses shared_memory_descriptor.reinterpret in chunk_kda gfx1250 (open)

</details>

<details>
<summary>Other (3)</summary>

- [#6192](https://github.com/ROCm/aiter/pull/6192) AgentX draft slot 1 (open, empty)
- [#6193](https://github.com/ROCm/aiter/pull/6193) AgentX draft slot 2 (open, empty)
- [#6194](https://github.com/ROCm/aiter/pull/6194) AgentX draft slot 3 (open, empty)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: af0af8538767a466e3f7fec9983e194fcb8595f6de4bd3c716d4df17ce850de7 -->
