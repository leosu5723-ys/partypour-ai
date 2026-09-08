# PartyPour AI — RAG Knowledge Base (v2.0, aligned to data source v1.8)

25 retrievable English knowledge chunks: 17 canonical cocktail recipes + 8 reference documents. This is the curated knowledge collection for Stage 4 (In-Context Learning / Lightweight RAG). Retrieval approach: exact-match / keyword retrieval on `chunk_id`, `title`, and `retrieval_keywords` — consistent with the project's own decision that a knowledge base this small does not need full vector search.

Note on scope: this knowledge base intentionally does NOT include raw SKU prices or supplier data. Prices and purchase quantities stay in the deterministic calculation module (reading the SKU Product Catalog directly); the language model only ever explains numbers the calculation module already produced, per the project's "Source of Truth" principle.

v2 change log: regenerated from the v1.8 data source (17 recipes, up from 10; Margarita is now a real supported drink — test case T03 now uses "Espresso Martini" as the unsupported-drink example instead; budget tiers are now rule-driven (budget/standard/premium) rather than a shared/tiered ingredient matrix; added REF-SAFETY-001 for the new egg-white allergen rule; REF-ASSUMPTIONS-001 documents the 7 new Singapore-localized package-yield assumptions).

---

## DRY_MARTINI_001 — Canonical Recipe: Dry Martini (干马天尼)

*Type: canonical_recipe | Retrieval keywords: dry martini, 干马天尼, gin, stir, nick & nora / cocktail glass, gin, dry vermouth*

```
Recipe ID: DRY_MARTINI_001
Name: Dry Martini (干马天尼)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Gin
Alcoholic: Yes
Glassware: Nick & Nora / Cocktail glass | Serving style: straight up
Ingredients (per serving):
  - Gin (金酒): 60 ml — Use chilled gin.
  - Dry Vermouth (不甜苦艾酒): 10 ml — Project ratio is 60:10.
Garnish: Olive or Lemon Twist (橄榄或柠檬皮), 1 piece (optional)
Method: Stir with ice, then strain into a chilled glass.
Ice preparation: Ice — 120 g per serving (preparation: Cooling and dilution for stir method.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed.
Source note: Project-standard draft; source and ratio must be confirmed by the team.
Team decision: Confirm 60 ml Gin + 10 ml Dry Vermouth.
```

---

## NEGRONI_001 — Canonical Recipe: Negroni (尼格罗尼)

*Type: canonical_recipe | Retrieval keywords: negroni, 尼格罗尼, gin, stir, old fashioned glass, gin, campari, sweet vermouth*

```
Recipe ID: NEGRONI_001
Name: Negroni (尼格罗尼)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Gin
Alcoholic: Yes
Glassware: Old Fashioned glass | Serving style: on the rocks
Ingredients (per serving):
  - Gin (金酒): 30 ml — Equal-parts draft.
  - Campari (金巴利): 30 ml — Equal-parts draft.
  - Sweet Vermouth (甜苦艾酒): 30 ml — Equal-parts draft.
Garnish: Orange Peel (橙皮), 1 piece
Method: Build or stir with ice, then serve over fresh ice.
Ice preparation: Ice — 180 g per serving (preparation: Serve over fresh ice.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
Recipe-specific substitution rules: SUB_CAMPARI_001: CAMPARI -> APEROL — NOT ALLOWED (requires user confirmation). Do not silently replace Campari with Aperol because bitterness and sweetness change the canonical Negroni profile.
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed.
Source note: Project-standard draft based on the equal-parts convention; verify the selected reference.
Team decision: Confirm 30 ml each of Gin, Campari and Sweet Vermouth.
```

---

## WHISKY_HIGHBALL_001 — Canonical Recipe: Whisky Highball (威士忌嗨棒)

*Type: canonical_recipe | Retrieval keywords: whisky highball, 威士忌嗨棒, whisky, build, highball glass, whisky, soda water*

```
Recipe ID: WHISKY_HIGHBALL_001
Name: Whisky Highball (威士忌嗨棒)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Whisky
Alcoholic: Yes
Glassware: Highball glass | Serving style: on the rocks
Ingredients (per serving):
  - Whisky (威士忌): 45 ml — Use a whisky selected by the team.
  - Soda Water (苏打水): 135 ml — Volume depends on glass and ice.
Garnish: Lemon Peel (柠檬皮), 1 piece (optional)
Method: Build over ice and top with chilled soda water.
Ice preparation: Ice — 180 g per serving (preparation: Build over ice.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed.
Source note: The Chinese name 嗨棒 is interpreted as Whisky Highball per team confirmation.
Team decision: Confirm whisky type and soda-water volume.
```

---

## GIN_TONIC_001 — Canonical Recipe: Gin & Tonic (金汤力)

*Type: canonical_recipe | Retrieval keywords: gin & tonic, 金汤力, gin, build, highball / copa glass, gin, tonic water*

```
Recipe ID: GIN_TONIC_001
Name: Gin & Tonic (金汤力)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Gin
Alcoholic: Yes
Glassware: Highball / Copa glass | Serving style: on the rocks
Ingredients (per serving):
  - Gin (金酒): 50 ml — Team-confirmed.
  - Tonic Water (汤力水): 150 ml — Team-confirmed.
Garnish: Lemon Slice or Lime Wedge (柠檬片或青柠角), 1 piece
Method: Build over ice, add tonic water slowly, and stir gently.
Ice preparation: Ice — 180 g per serving (preparation: Large amount of ice for highball.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed.
Source note: Team-confirmed fixed volume for MVP.
Team decision: Use 50 ml Gin + 150 ml Tonic Water.
```

---

## DAIQUIRI_001 — Canonical Recipe: Daiquiri (得其利)

*Type: canonical_recipe | Retrieval keywords: daiquiri, 得其利, white rum, shake, coupe / cocktail glass, white rum, lime juice, simple syrup*

```
Recipe ID: DAIQUIRI_001
Name: Daiquiri (得其利)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: White Rum
Alcoholic: Yes
Glassware: Coupe / Cocktail glass | Serving style: straight up
Ingredients (per serving):
  - White Rum (白朗姆酒): 60 ml — Shake with ice.
  - Lime Juice (青柠汁): 20 ml — Fresh or packaged; product mapping later.
  - Simple Syrup (糖浆): 20 ml — Use one project-wide syrup definition.
Garnish: Lime Wheel (青柠轮片), 1 piece (optional)
Method: Shake with ice and strain into a chilled glass.
Ice preparation: Ice — 120 g per serving (preparation: Shake method.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed. | SUB_LIME_001 (any recipe): fresh Lime Juice -> bottled Lime Juice is allowed at any tier but REQUIRES user confirmation (disclosed convenience swap). | SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: Project-standard draft; verify against the selected reference.
Team decision: Use 60 ml Rum + 20 ml Lime Juice + 20 ml Simple Syrup.
```

---

## WHISKEY_SOUR_001 — Canonical Recipe: Whiskey Sour (威士忌酸)

*Type: canonical_recipe | Retrieval keywords: whiskey sour, 威士忌酸, bourbon, shake, old fashioned glass, bourbon, lemon juice, simple syrup, egg white*

```
Recipe ID: WHISKEY_SOUR_001
Name: Whiskey Sour (威士忌酸)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Bourbon
Alcoholic: Yes
Glassware: Old Fashioned glass | Serving style: on the rocks
Ingredients (per serving):
  - Bourbon (波本威士忌): 60 ml — Use Bourbon as the MVP whiskey.
  - Lemon Juice (柠檬汁): 30 ml — Fresh or packaged; product mapping later.
  - Simple Syrup (糖浆): 20 ml — Project-wide syrup definition.
  - Egg White (蛋清): 15 ml — Dry shake first; allergen and food-safety note required.
Garnish: Lemon Peel or Cherry (柠檬皮或樱桃), 1 piece
Method: Dry shake with egg white, then shake with ice and strain over fresh ice.
Ice preparation: Ice — 120 g per serving (preparation: Shake and serve over fresh ice.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
Recipe-specific substitution rules: SUB_EGG_001: EGG_WHITE -> PASTEURISED_EGG_WHITE — ALLOWED (no confirmation needed). Pasteurised egg white keeps the intended texture while improving food-safety handling.
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed. | SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: Egg white is intentionally included per team decision; allergen and food-safety note required.
Team decision: Use 60 ml Bourbon + 30 ml Lemon Juice + 20 ml Simple Syrup + 15 ml Egg White.
Food-safety note (SAFE_001): this recipe contains egg white — the system must show an allergen warning whenever this recipe appears in a recommendation.
```

---

## MOSCOW_MULE_001 — Canonical Recipe: Moscow Mule (莫斯科骡子)

*Type: canonical_recipe | Retrieval keywords: moscow mule, 莫斯科骡子, vodka, build, mule mug / highball glass, vodka, ginger beer, lime juice*

```
Recipe ID: MOSCOW_MULE_001
Name: Moscow Mule (莫斯科骡子)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Vodka
Alcoholic: Yes
Glassware: Mule mug / Highball glass | Serving style: on the rocks
Ingredients (per serving):
  - Vodka (伏特加): 50 ml — Use neutral vodka.
  - Ginger Beer (姜汁啤酒): 120 ml — Do not merge with Ginger Ale.
  - Lime Juice (青柠汁): 15 ml — Fresh or packaged.
Garnish: Lime Wedge (青柠角), 1 piece
Method: Build over ice, add ginger beer, and stir gently.
Ice preparation: Ice — 180 g per serving (preparation: Build over ice.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed. | SUB_LIME_001 (any recipe): fresh Lime Juice -> bottled Lime Juice is allowed at any tier but REQUIRES user confirmation (disclosed convenience swap). | SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: Project-standard draft; keep Ginger Beer distinct from Ginger Ale.
Team decision: Confirm 50 ml Vodka + 120 ml Ginger Beer + 15 ml Lime Juice.
```

---

## TOM_COLLINS_001 — Canonical Recipe: Tom Collins (汤姆柯林斯)

*Type: canonical_recipe | Retrieval keywords: tom collins, 汤姆柯林斯, gin, shake_build, collins glass, gin, lemon juice, simple syrup, soda water*

```
Recipe ID: TOM_COLLINS_001
Name: Tom Collins (汤姆柯林斯)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Gin
Alcoholic: Yes
Glassware: Collins glass | Serving style: on the rocks
Ingredients (per serving):
  - Gin (金酒): 45 ml — Shake with citrus and syrup.
  - Lemon Juice (柠檬汁): 30 ml — Fresh or packaged.
  - Simple Syrup (糖浆): 15 ml — Project-wide syrup definition.
  - Soda Water (苏打水): 90 ml — Volume depends on glass and ice.
Garnish: Lemon Slice and Cherry (柠檬片和樱桃), 2 pieces
Method: Shake Gin, lemon juice and syrup with ice; strain over ice and top with soda.
Ice preparation: Ice — 180 g per serving (preparation: Serve over fresh ice.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed. | SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: Project-standard draft; soda volume is an estimate tied to glass size.
Team decision: Use 45 ml Gin + 30 ml Lemon Juice + 15 ml Simple Syrup + 90 ml Soda Water.
```

---

## CUBA_LIBRE_001 — Canonical Recipe: Cuba Libre (自由古巴)

*Type: canonical_recipe | Retrieval keywords: cuba libre, 自由古巴, dark rum, build, highball glass, dark rum, cola, lime juice*

```
Recipe ID: CUBA_LIBRE_001
Name: Cuba Libre (自由古巴)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Dark Rum
Alcoholic: Yes
Glassware: Highball glass | Serving style: on the rocks
Ingredients (per serving):
  - Dark Rum (黑朗姆酒): 50 ml — Use dark rum for project canonical version.
  - Cola (可乐): 120 ml — Use cola, not soda water.
  - Lime Juice (青柠汁): 10 ml — Canonical citrus is lime.
Garnish: Lime Wedge (青柠角), 1 piece
Method: Build over ice, add lime juice and cola, then stir gently.
Ice preparation: Ice — 180 g per serving (preparation: Build over ice.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed. | SUB_LIME_001 (any recipe): fresh Lime Juice -> bottled Lime Juice is allowed at any tier but REQUIRES user confirmation (disclosed convenience swap). | SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: Project-standard draft; use lime rather than lemon for the canonical version.
Team decision: Confirm 50 ml Dark Rum + 120 ml Cola + 10 ml Lime Juice.
```

---

## MOJITO_001 — Canonical Recipe: Mojito (莫吉托)

*Type: canonical_recipe | Retrieval keywords: mojito, 莫吉托, white rum, muddle_build, highball glass, white rum, lime juice, simple syrup, mint leaves, soda water*

```
Recipe ID: MOJITO_001
Name: Mojito (莫吉托)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: White Rum
Alcoholic: Yes
Glassware: Highball glass | Serving style: on the rocks
Ingredients (per serving):
  - White Rum (白朗姆酒): 45 ml — Use white rum for project canonical version.
  - Lime Juice (青柠汁): 20 ml — Fresh or packaged.
  - Simple Syrup (糖浆): 15 ml — Use syrup rather than loose sugar.
  - Mint Leaves (薄荷叶): 6 leaves — Gently muddle; do not shred aggressively.
  - Soda Water (苏打水): 75 ml — Top up after crushed ice.
Garnish: Mint Sprig and Lime Wedge (薄荷枝和青柠角), 2 pieces
Method: Muddle lime, mint and syrup gently; add rum, crushed ice and soda.
Ice preparation: Crushed Ice — 220 g per serving (preparation: Muddle/build method.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed. | SUB_LIME_001 (any recipe): fresh Lime Juice -> bottled Lime Juice is allowed at any tier but REQUIRES user confirmation (disclosed convenience swap). | SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: Project-standard draft; use Simple Syrup for machine-readable consistency.
Team decision: Use 45 ml White Rum + 20 ml Lime Juice + 15 ml Simple Syrup + 75 ml Soda Water.
```

---

## COSMOPOLITAN_001 — Canonical Recipe: Cosmopolitan (大都会)

*Type: canonical_recipe | Retrieval keywords: cosmopolitan, 大都会, vodka, shake, cocktail glass, citrus vodka, triple sec, cranberry juice, lime juice*

```
Recipe ID: COSMOPOLITAN_001
Name: Cosmopolitan (大都会)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Vodka
Alcoholic: Yes
Glassware: Cocktail glass | Serving style: straight up
Ingredients (per serving):
  - Citrus Vodka (柑橘伏特加): 40 ml — May map to neutral vodka as a product substitution only if approved.
  - Triple Sec (橙味利口酒): 15 ml — Orange liqueur.
  - Cranberry Juice (蔓越莓汁): 30 ml — Use cranberry juice, not cranberry syrup.
  - Lime Juice (青柠汁): 15 ml — Fresh or packaged.
Garnish: Orange Peel (橙皮), 1 piece
Method: Shake all liquid ingredients with ice and strain into a chilled glass.
Ice preparation: Ice — 120 g per serving (preparation: Shake method.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed. | SUB_LIME_001 (any recipe): fresh Lime Juice -> bottled Lime Juice is allowed at any tier but REQUIRES user confirmation (disclosed convenience swap). | SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: Project-standard draft; Citrus Vodka is a product-level choice that may map to Vodka.
Team decision: Confirm 40 ml Citrus Vodka + 15 ml Triple Sec + 30 ml Cranberry Juice + 15 ml Lime Juice.
```

---

## GODFATHER_001 — Canonical Recipe: Godfather (教父)

*Type: canonical_recipe | Retrieval keywords: godfather, 教父, scotch whisky, stir, old fashioned glass, scotch whisky, amaretto*

```
Recipe ID: GODFATHER_001
Name: Godfather (教父)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Scotch Whisky
Alcoholic: Yes
Glassware: Old Fashioned glass | Serving style: on the rocks
Ingredients (per serving):
  - Scotch Whisky (苏格兰威士忌): 45 ml — Use Scotch as the canonical base.
  - Amaretto (杏仁利口酒): 15 ml — Almond-flavoured liqueur.
Garnish: Orange Peel (橙皮), 1 piece (optional)
Method: Stir Scotch and Amaretto with ice and serve over fresh ice.
Ice preparation: Ice — 180 g per serving (preparation: Stir and serve over fresh ice.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed.
Source note: Project-standard draft; verify the selected ratio.
Team decision: Use 45 ml Scotch + 15 ml Amaretto.
```

---

## MARGARITA_001 — Canonical Recipe: Margarita (玛格丽特)

*Type: canonical_recipe | Retrieval keywords: margarita, 玛格丽特, tequila, shake, coupe / margarita glass, tequila, triple sec, lime juice, salt*

```
Recipe ID: MARGARITA_001
Name: Margarita (玛格丽特)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Tequila
Alcoholic: Yes
Glassware: Coupe / Margarita glass | Serving style: straight up or on the rocks
Ingredients (per serving):
  - Tequila (龙舌兰酒): 50 ml — Use Blanco Tequila for MVP unless team approves another style.
  - Triple Sec (橙味利口酒): 20 ml — Orange liqueur.
  - Lime Juice (青柠汁): 20 ml — Fresh or packaged.
  - Salt (盐): 1 g (optional) — Only for optional salt rim.
Garnish: Lime Wheel (青柠轮片), 1 piece
Method: Optional salt the rim; shake liquid ingredients with ice and strain.
Ice preparation: Ice — 120 g per serving (preparation: Shake method.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed. | SUB_LIME_001 (any recipe): fresh Lime Juice -> bottled Lime Juice is allowed at any tier but REQUIRES user confirmation (disclosed convenience swap). | SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: Project-standard draft; salt rim is modeled as optional garnish material.
Team decision: Use 50 ml Tequila + 20 ml Triple Sec + 20 ml Lime Juice.
```

---

## OLD_FASHIONED_001 — Canonical Recipe: Old Fashioned (古典)

*Type: canonical_recipe | Retrieval keywords: old fashioned, 古典, bourbon or rye whiskey, stir, old fashioned glass, bourbon or rye whiskey, simple syrup, angostura bitters*

```
Recipe ID: OLD_FASHIONED_001
Name: Old Fashioned (古典)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: Bourbon or Rye Whiskey
Alcoholic: Yes
Glassware: Old Fashioned glass | Serving style: on the rocks
Ingredients (per serving):
  - Bourbon or Rye Whiskey (波本或黑麦威士忌): 60 ml — Team should decide whether to allow both styles.
  - Simple Syrup (糖浆): 7.5 ml — Project-wide syrup definition.
  - Angostura Bitters (安格式苦精): 2 dashes — Dash is an estimated dispensing unit.
Garnish: Orange Peel (橙皮), 1 piece
Method: Stir whiskey, syrup and bitters with ice; serve over a large cube.
Ice preparation: Ice — 180 g per serving (preparation: Serve over a large cube if available.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed.
Source note: Project-standard draft; bitters are recorded in dashes and estimated for procurement.
Team decision: Use 60 ml Whiskey + 7.5 ml Simple Syrup + 2 dashes Bitters.
```

---

## SINGAPORE_SLING_001 — Canonical Recipe: Singapore Sling (新加坡司令)

*Type: canonical_recipe | Retrieval keywords: singapore sling, 新加坡司令, gin, shake, hurricane glass, gin, cherry sangue morlacco, cointreau, benedictine dom, fresh pineapple juice, fresh lime juice, grenadine syrup, angostura bitters*

```
Recipe ID: SINGAPORE_SLING_001
Name: Singapore Sling (新加坡司令)
Version: 1.0
Status: canonical (source_status: verified)
Base spirit: Gin
Alcoholic: Yes
Glassware: Hurricane glass | Serving style: on the rocks
Ingredients (per serving):
  - Gin (金酒): 30 ml — IBA official ingredient.
  - Cherry Sangue Morlacco (樱桃利口酒（Sangue Morlacco）): 15 ml — IBA official ingredient.
  - Cointreau (君度橙酒): 7.5 ml — IBA official ingredient.
  - Benedictine DOM (贝内迪克汀 DOM): 7.5 ml — IBA official ingredient.
  - Fresh Pineapple Juice (新鲜菠萝汁): 120 ml — IBA official ingredient.
  - Fresh Lime Juice (新鲜青柠汁): 15 ml — IBA official ingredient.
  - Grenadine Syrup (石榴糖浆): 10 ml — IBA official ingredient.
  - Angostura Bitters (安格式苦精): 1 dash — IBA official ingredient; dash is a dispensing unit.
Garnish: Pineapple Wedge and Maraschino Cherry (菠萝片和马拉斯奇诺樱桃), 2 pieces
Method: Shake all ingredients with ice and strain into a Hurricane glass.
Ice preparation: Ice — 180 g per serving (preparation: Planning assumption for shaking and serving.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
Recipe-specific substitution rules: SUB_COIN_001: COINTREAU -> TRIPLE_SEC — ALLOWED (requires user confirmation). Budget substitution is possible, but the exact IBA Cointreau ingredient should be preferred. | SUB_CHERRY_001: CHERRY_SANGUE_MORLACCO -> CHERRY_LIQUEUR — ALLOWED (requires user confirmation). Bols Cherry Brandy is a practical substitute but is not identical to Cherry Sangue Morlacco.
General substitution rules that also apply: SUB_BRAND_001 (any recipe): a same-base-spirit-category brand/package swap is allowed at any budget tier, no confirmation needed. | SUB_LIME_001 (any recipe): fresh Lime Juice -> bottled Lime Juice is allowed at any tier but REQUIRES user confirmation (disclosed convenience swap). | SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: IBA official recipe selected by the team; no soda water is included.
Team decision: Use the IBA version: 30 Gin + 15 Cherry Sangue Morlacco + 7.5 Cointreau + 7.5 Benedictine + 120 Pineapple Juice + 15 Lime Juice + 10 Grenadine + 1 dash Angostura.
```

---

## CINDERELLA_001 — Canonical Recipe: Cinderella (灰姑娘（无酒精）)

*Type: canonical_recipe | Retrieval keywords: cinderella, 灰姑娘（无酒精）, non-alcoholic, shake_build, highball glass, lemon juice, orange juice, pineapple juice, grenadine, soda water*

```
Recipe ID: CINDERELLA_001
Name: Cinderella (灰姑娘（无酒精）)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: None
Alcoholic: No (mocktail)
Glassware: Highball glass | Serving style: on the rocks
Ingredients (per serving):
  - Lemon Juice (柠檬汁): 30 ml — Fresh or packaged.
  - Orange Juice (橙汁): 30 ml — Fresh or packaged.
  - Pineapple Juice (菠萝汁): 30 ml — Fresh or packaged.
  - Grenadine (石榴糖浆): 10 ml — Non-alcoholic syrup.
  - Soda Water (苏打水): 90 ml — May be replaced by lemon-lime soda only through an explicit rule.
Garnish: Orange Slice or Cherry (橙片或樱桃), 1 piece
Method: Shake fruit juices and syrup with ice; strain over ice and top with soda or lemon-lime soda.
Ice preparation: Ice — 180 g per serving (preparation: Build over ice.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
Recipe-specific substitution rules: SUB_SODA_001: SODA_WATER -> LEMON_LIME_SODA — ALLOWED (requires user confirmation). Only allowed after user confirmation because sweetness changes the drink balance.
General substitution rules that also apply: SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: Non-alcoholic option; verify the selected soda component and quantity.
Team decision: Use 30 ml Lemon Juice + 30 ml Orange Juice + 30 ml Pineapple Juice + 10 ml Grenadine + 90 ml Soda Water.
```

---

## VIRGIN_MOJITO_001 — Canonical Recipe: Virgin Mojito (无酒精莫吉托)

*Type: canonical_recipe | Retrieval keywords: virgin mojito, 无酒精莫吉托, non-alcoholic, muddle_build, highball glass, lime juice, simple syrup, mint leaves, soda water*

```
Recipe ID: VIRGIN_MOJITO_001
Name: Virgin Mojito (无酒精莫吉托)
Version: 1.0
Status: draft_canonical (source_status: candidate)
Base spirit: None
Alcoholic: No (mocktail)
Glassware: Highball glass | Serving style: on the rocks
Ingredients (per serving):
  - Lime Juice (青柠汁): 25 ml — Fresh or packaged.
  - Simple Syrup (糖浆): 15 ml — Project-wide syrup definition.
  - Mint Leaves (薄荷叶): 6 leaves — Gently muddle.
  - Soda Water (苏打水): 120 ml — Top up after crushed ice.
Garnish: Mint Sprig and Lime Wedge (薄荷枝和青柠角), 2 pieces
Method: Muddle lime, mint and syrup gently; add crushed ice and soda.
Ice preparation: Crushed Ice — 220 g per serving (preparation: Muddle/build method.; before the project's 10% ICE_WASTAGE_BUFFER_PCT wastage buffer)
General substitution rules that also apply: SUB_LIME_001 (any recipe): fresh Lime Juice -> bottled Lime Juice is allowed at any tier but REQUIRES user confirmation (disclosed convenience swap). | SUB_JUICE_001 (any recipe): fresh juice -> packaged juice is allowed at any tier but REQUIRES user confirmation (may change freshness/flavour).
Source note: Non-alcoholic option designed to share ingredients with Mojito.
Team decision: Use 25 ml Lime Juice + 15 ml Simple Syrup + 6 mint leaves + 120 ml Soda Water.
```

---

## REF-MENU-001 — Supported Menu and Unsupported Drink Policy

*Type: reference | Retrieval keywords: supported menu, unsupported drink, unknown drink, espresso martini, margarita, unsupported_drinks, menu policy*

```
Supported menu (17 canonical drinks, v1.8 data source):
Dry Martini (干马天尼, DRY_MARTINI_001) — alcoholic, status: draft_canonical
Negroni (尼格罗尼, NEGRONI_001) — alcoholic, status: draft_canonical
Whisky Highball (威士忌嗨棒, WHISKY_HIGHBALL_001) — alcoholic, status: draft_canonical
Gin & Tonic (金汤力, GIN_TONIC_001) — alcoholic, status: draft_canonical
Daiquiri (得其利, DAIQUIRI_001) — alcoholic, status: draft_canonical
Whiskey Sour (威士忌酸, WHISKEY_SOUR_001) — alcoholic, status: draft_canonical
Moscow Mule (莫斯科骡子, MOSCOW_MULE_001) — alcoholic, status: draft_canonical
Tom Collins (汤姆柯林斯, TOM_COLLINS_001) — alcoholic, status: draft_canonical
Cuba Libre (自由古巴, CUBA_LIBRE_001) — alcoholic, status: draft_canonical
Mojito (莫吉托, MOJITO_001) — alcoholic, status: draft_canonical
Cosmopolitan (大都会, COSMOPOLITAN_001) — alcoholic, status: draft_canonical
Godfather (教父, GODFATHER_001) — alcoholic, status: draft_canonical
Margarita (玛格丽特, MARGARITA_001) — alcoholic, status: draft_canonical
Old Fashioned (古典, OLD_FASHIONED_001) — alcoholic, status: draft_canonical
Singapore Sling (新加坡司令, SINGAPORE_SLING_001) — alcoholic, status: canonical
Cinderella (灰姑娘（无酒精）, CINDERELLA_001) — non-alcoholic, status: draft_canonical
Virgin Mojito (无酒精莫吉托, VIRGIN_MOJITO_001) — non-alcoholic, status: draft_canonical

System rule: if a user requests a drink that is not on this list, the
system must NOT invent or improvise a recipe from the model's general
knowledge. The requested name must be placed in an `unsupported_drinks`
field, and the user should be prompted to choose from the supported menu
instead.

Reference example: Espresso Martini is used throughout the
project's test cases as the standard example of an "unsupported drink"
request. NOTE (v1.8 change): Margarita is NOW a real, fully supported
canonical recipe in this data source (MARGARITA_001) — it used to be the
project's standard "unsupported drink" example in the earlier v1.2
catalog, but that changed when the team's recipe dataset was expanded
from 10 to 17 drinks. Test case T03 was updated
accordingly to use "Espresso Martini" instead, which is
genuinely not on this menu. Do not treat Margarita as unsupported.
```

---

## REF-TIER-001 — Budget Tier System Reference (rule-driven, v1.8)

*Type: reference | Retrieval keywords: budget tier, economy, balanced, quality, budget, standard, premium, budget mode, tier selection, base spirit*

```
TIER_001 (tier_selection): when requested_plan equals 'budget' -> select_base_tier = 'budget'. User-facing label: '经济型'. 只选择基酒的 budget SKU；其他材料继续使用 value_default。

TIER_002 (tier_selection): when requested_plan equals 'standard' -> select_base_tier = 'standard'. User-facing label: '平衡型'. 只选择基酒的 standard SKU；作为未指定预算时的默认方案。

TIER_003 (tier_selection): when requested_plan equals 'premium' -> select_base_tier = 'premium'. User-facing label: '高端型'. 只选择基酒的 premium SKU；其他材料不自动升级。

TIER_004 (tier_selection): when requested_plan is_empty None -> select_base_tier = 'standard'. User-facing label: '平衡型'. 用户没有说明预算时，默认使用中等档位基酒。

BASE_001 (ingredient_selection): when product_category equals 'base_spirit' -> allow_tier_options = 'true'. User-facing label: '基酒三档'. 只有基酒允许根据预算返回三个品牌选项。

NONBASE_001 (ingredient_selection): when product_category in 'modifier|mixer|garnish_material|food_ingredient' -> select_default_sku = 'true'. User-facing label: '其他材料默认性价比'. 利口酒、软饮、果汁、糖浆、冰块和装饰材料不参与三档升级。

SUB_001 (ingredient_selection): when mapping_type equals 'value_default' -> do_not_silently_replace_exact = 'true'. User-facing label: '禁止静默替换'. 如果配方要求指定品牌或指定材料，替代品必须显示为 substitution_candidate。

Summary: the system supports three budget tiers — budget (经济型),
standard (平衡型, the default when the user does not state a budget tier),
and premium (高端型). ONLY ingredients in the `base_spirit` product
category (the recipe's main spirit) carry three separate tier options;
every other ingredient (modifier, mixer, garnish_material,
food_ingredient — liqueurs, juices, syrups, ice, garnishes) uses one
fixed "value_default" product regardless of tier (rule NONBASE_001). A
substitution must never silently replace an ingredient the recipe
specifies exactly (rule SUB_001) — it must be surfaced as a
substitution_candidate for the user to accept.
```

---

## REF-CALC-001 — Procurement Calculation and Package-Size Rules (v1.8)

*Type: reference | Retrieval keywords: packaging, rounding, purchase quantity, leftover, price range, calculation rule, package size, out of stock, fallback*

```
QTY_001 (procurement_calculation): when required_volume_ml greater_than '0' -> packages_needed = 'ceil(required_volume_ml / package_size_ml)'. 所需总量除以包装容量后向上取整，不能购买半瓶。

QTY_002 (procurement_calculation): when package_size_ml equals '0|empty' -> flag_data_issue = 'package_size_missing'. 没有包装容量时不输出购买数量，先标记数据问题。

PRICE_001 (recommendation_quality): when unit_price_sgd is_empty None -> exclude_from_cost_total = 'true'. 价格缺失时可以展示品牌，但不能进入总价排序。

STOCK_001 (recommendation_quality): when availability_sg equals 'back_soon_observed|out_of_stock' -> fallback_same_tier = 'true'. 当前商品缺货时，优先选择同一基酒类别和同一价格档位的可售 SKU。

These rules govern the deterministic calculation module. The language
model must never perform this arithmetic itself or state a number that
was not produced by this module.

1. Total ingredient need = amount_value x planned_servings, summed across
   every recipe in the order that shares the same ingredient_id (e.g. Gin
   needed for Dry Martini, Negroni, and Gin & Tonic is combined into one
   total before rounding).
2. Purchase quantity = ceiling(total_amount_needed / package_size) — QTY_001.
   A missing package size is a data problem to flag (QTY_002), never a
   number to guess.
3. Leftover = (purchase_quantity x package_size) - total_amount_needed.
4. Package sizes for the small set of weight/count-based garnish and
   mixer items (ice, egg white, simple syrup made from raw sugar, fresh
   lemon/lime/orange used for peel/wedge/wheel/juice, olives, maraschino
   cherries) are NOT stored as a separate spreadsheet column by team
   decision (v1.8) — the raw package weight already lives in the SKU's
   product_name text (e.g. "650g", "2kg equivalent") and is parsed by the
   loader, then combined with the matching ratio in the Assumptions sheet
   (see REF-ASSUMPTIONS-001) to get a usable procurement quantity.
5. unit_price_sgd is a fixed snapshot (Singapore dollars, Lazada
   Singapore / RedMart sourced, checked 2026-09-05), not a live price. An
   ingredient with no price is excluded from the cost total but its
   brand may still be shown (PRICE_001) — as of v1.8 every SKU has a
   price, so this mainly matters if a future SKU is added without one.
6. If a chosen SKU is out of stock or "back soon", fall back to another
   available SKU in the same base-spirit category and the same price
   tier (STOCK_001) rather than silently switching category or tier.
```

---

## REF-ASSUMPTIONS-001 — Ice Method, Citrus Yield and Package-Conversion Assumptions (v1.8)

*Type: reference | Retrieval keywords: ice, crushed ice, lemon yield, lime yield, orange weight, egg white density, simple syrup yield, cherry count, olive count, garnish quantity, wastage buffer, planning assumption, singapore*

```
These are team planning assumptions for the course MVP, not measured
facts, and should be described to the user as such.

Reference ice methods (illustrative — each recipe's actual ICE_CUBES /
CRUSHED_ICE amount is baked directly into the Recipe Ingredients sheet
and may differ slightly from these reference values when a recipe is
served "on the rocks" and needs extra ice in the glass, not just for
mixing):
  - Direct build or highball over ice (BUILD_OVER_ICE): 180 g/serving — Use for Gin & Tonic, Whisky Highball, Cuba Libre and similar drinks.
  - Stir with ice and strain (STIR_AND_STRAIN): 120 g/serving — Use for Dry Martini, Negroni, Godfather and Old Fashioned chilling.
  - Shake with ice and strain (SHAKE_AND_STRAIN): 150 g/serving — Use for Daiquiri, Margarita, Cosmopolitan and Singapore Sling.
  - Muddle and serve with crushed ice (MUDDLE_CRUSHED): 220 g/serving — Use for Mojito and Virgin Mojito.

Full Assumptions table (19 entries, includes 7 new
Singapore-localized entries added when the data source moved to v1.8 —
see the file's own rationale column for full sourcing):
  - PRICE_BUFFER_PCT = 0.1 ratio — Prices can change because of promotions, supplier and channel differences.
  - ICE_WASTAGE_BUFFER_PCT = 0.1 ratio — Adds a practical buffer for melting, transfer and service loss.
  - LEMON_YIELD_ML_PER_PC = 30 ml/pc — Converts recipe juice volume into whole-fruit purchasing quantity.
  - LIME_YIELD_ML_PER_PC = 20 ml/pc — Converts recipe juice volume into whole-fruit purchasing quantity.
  - PINEAPPLE_GARNISH_SLICES_PER_PC = 12 slices/pc — Estimates garnish pieces available from one pineapple.
  - BITTERS_DASH_ML = 0.8 ml/dash — Makes dash-based recipes machine-readable for procurement.
  - MINT_LEAVES_PER_BUNCH = 40 leaves/bunch — Converts leaf counts into bunches for procurement.
  - BUILD_OVER_ICE_G_PER_SERVING = 180 g/serving — Ice used for direct-build and highball service.
  - STIR_AND_STRAIN_G_PER_SERVING = 120 g/serving — Ice used for chilling and dilution before straining.
  - SHAKE_AND_STRAIN_G_PER_SERVING = 150 g/serving — Ice used for shaking and chilling before straining.
  - MUDDLE_CRUSHED_G_PER_SERVING = 220 g/serving — Higher quantity accounts for crushed-ice service.
  - FRUIT_PURCHASE_ROUNDING = 1 whole unit — Fresh produce is purchased in whole units and rounded up.
  - LEMON_AVG_WEIGHT_G = 120 g/pc — Converts lemon-weight packs (e.g. RedMart Unwaxed Lemons 650g) into a piece count for procurement math.
  - LIME_AVG_WEIGHT_G = 75 g/pc — Converts lime-weight packs (250g) into a piece count for procurement math.
  - ORANGE_AVG_WEIGHT_G = 180 g/pc — Converts orange-weight packs (RedMart Navel Orange 850g) into a piece count for procurement math.
  - EGG_WHITE_DENSITY_G_PER_ML = 1.03 g/ml — Converts the 420g frozen pasteurised egg-white pack into ~408ml for recipes that use ml (e.g. Whiskey Sour).
  - SUGAR_TO_SYRUP_YIELD_ML_PER_G = 1.65 ml finished syrup / g sugar — Converts the RedMan Syrup Sugar 700g pack into ~1155ml of finished simple syrup for procurement math.
  - CHERRY_COUNT_PER_G = 0.1625 pieces/g — Converts the Domee Red Maraschino Cherry 727g jar into ~118 garnish pieces for procurement math.
  - OLIVE_COUNT_PER_350G_JAR = 45 pieces/jar — Converts the Borges Whole Green Olives 350g jar into ~45 garnish pieces for procurement math.

The 7 newest entries (LEMON_AVG_WEIGHT_G, LIME_AVG_WEIGHT_G,
ORANGE_AVG_WEIGHT_G, EGG_WHITE_DENSITY_G_PER_ML,
SUGAR_TO_SYRUP_YIELD_ML_PER_G, CHERRY_COUNT_PER_G,
OLIVE_COUNT_PER_350G_JAR) exist specifically to convert the raw package
weight printed in a SKU's product_name (e.g. "RedMart Unwaxed Lemons
650g") into a usable procurement quantity, since the SKU Product Catalog
does not carry a separate structured column for that. Two of them
(CHERRY_COUNT_PER_G, OLIVE_COUNT_PER_350G_JAR) are lower-confidence
cross-brand or mid-range retail estimates and are flagged as such —
this should be disclosed if a user asks how a garnish-purchase quantity
was derived.
```

---

## REF-SUBS-001 — Structured Substitution and Rejection Rules Reference (v1.8)

*Type: reference | Retrieval keywords: substitution rule, allowed substitution, rejected substitution, aperol, campari, rule validator, wildcard recipe*

```
Only the substitutions listed below are permitted. The rule-validator
module treats this table as the single source of truth; free-text notes
elsewhere are not a basis for approving a substitution. A recipe_id of
'*' means the rule applies to every recipe that contains a matching
ingredient, not just one named drink.

SUB_BRAND_001 — recipe: *, base_spirit -> same_base_spirit. ALLOWED (tiers: budget|standard|premium), no confirmation needed, canonical fidelity: high. Brand and package changes are allowed within the same base-spirit category when the selected tier is explicit.

SUB_JUICE_001 — recipe: *, fresh_juice -> packaged_juice. ALLOWED (tiers: budget|standard|premium), requires user confirmation, canonical fidelity: medium. Packaged juice can reduce preparation effort but may change freshness and flavour.

SUB_COIN_001 — recipe: SINGAPORE_SLING_001, COINTREAU -> TRIPLE_SEC. ALLOWED (tiers: budget), requires user confirmation, canonical fidelity: medium. Budget substitution is possible, but the exact IBA Cointreau ingredient should be preferred.

SUB_CHERRY_001 — recipe: SINGAPORE_SLING_001, CHERRY_SANGUE_MORLACCO -> CHERRY_LIQUEUR. ALLOWED (tiers: budget|standard|premium), requires user confirmation, canonical fidelity: medium. Bols Cherry Brandy is a practical substitute but is not identical to Cherry Sangue Morlacco.

SUB_CAMPARI_001 — recipe: NEGRONI_001, CAMPARI -> APEROL. NOT ALLOWED, requires user confirmation, canonical fidelity: low. Do not silently replace Campari with Aperol because bitterness and sweetness change the canonical Negroni profile.

SUB_SODA_001 — recipe: CINDERELLA_001, SODA_WATER -> LEMON_LIME_SODA. ALLOWED (tiers: budget|standard|premium), requires user confirmation, canonical fidelity: medium. Only allowed after user confirmation because sweetness changes the drink balance.

SUB_EGG_001 — recipe: WHISKEY_SOUR_001, EGG_WHITE -> PASTEURISED_EGG_WHITE. ALLOWED (tiers: budget|standard|premium), no confirmation needed, canonical fidelity: high. Pasteurised egg white keeps the intended texture while improving food-safety handling.

SUB_LIME_001 — recipe: *, LIME_JUICE -> BOTTLED_LIME_JUICE. ALLOWED (tiers: budget|standard|premium), requires user confirmation, canonical fidelity: medium. Fresh lime is preferred; bottled juice is a convenience substitution and must be disclosed.

The most important rejection to remember: SUB_CAMPARI_001 explicitly
rejects Negroni's Campari -> Aperol swap, even though Aperol is a common
"lighter Negroni" substitution in general bartending knowledge. This is
the project's standing example of the system refusing a plausible-
sounding but non-canonical request.
```

---

## REF-SAFETY-001 — Food-Safety and Allergen Warning Rule (v1.8, new)

*Type: reference | Retrieval keywords: allergen, egg white, food safety, whiskey sour, warning*

```
SAFE_001 (service_safety rule): when a recommended recipe contains egg
white as an ingredient (currently: Whiskey Sour, WHISKEY_SOUR_001), the
system must display an allergen and food-safety warning alongside the
recommendation. This is a new rule introduced with the v1.8 data source
schema (the Budget Tier Rules sheet's service_safety rule group) and did
not exist in the project's earlier v1.2 catalog, since no earlier
canonical recipe used egg white.

Related note: the project's Substitution Rules table also records
SUB_EGG_001, which allows (and does not require confirmation for)
substituting raw egg white with pasteurised egg white
(SKU_EGG_WHITE_VALUE_001) — pasteurised egg white is in fact the only
egg-white SKU in the catalog, chosen specifically to keep the intended
texture while improving food-safety handling for guests.
```

---

## REF-RESPONSIBLE-001 — Responsible Drinking and Non-Alcoholic Guidance

*Type: reference | Retrieval keywords: responsible drinking, non-alcoholic, mocktail, moderation, out of scope, safety boundary, virgin mojito, cinderella*

```
Standard responsible-serving reminder (general guidance, not medical
advice): serve alcohol in moderation, always keep water and at least one
non-alcoholic option available, and do not continue serving a guest who
appears intoxicated.

Non-alcoholic options (v1.8 has two, up from one in the earlier
catalog): Cinderella (CINDERELLA_001), Virgin Mojito (VIRGIN_MOJITO_001). Virgin Mojito is new in v1.8 and was
specifically designed to share most of its ingredients with the
alcoholic Mojito (lime juice, simple syrup, mint, soda water), so
ordering both at once benefits from the same shared-ingredient
consolidation the project's calculation engine already does for
alcoholic drinks.

Explicit scope boundary: the system does not estimate an individual's
alcohol tolerance, does not track personal drinking history, and does
not make personal health or safety judgments about any guest. Those
tasks are explicitly out of scope for this project — the system's job
stops at helping the organizer plan and purchase, not at deciding what
any individual guest should drink.
```

---

## REF-OUTPUT-001 — Purchase List Output Format and Budget Mode Descriptions

*Type: reference | Retrieval keywords: purchase list, output format, shopping list, budget mode description, cost estimate, bilingual*

```
Expected purchase list output, per party plan:
  - Ingredient/product list: each line shows the product name, quantity
    to buy (in purchase units, e.g. "2 x 700 ml bottles"), and the
    resulting leftover amount.
  - Estimated total cost: shown with the understanding that
    unit_price_sgd is a fixed Lazada Singapore / RedMart snapshot, not a
    live price, and may differ from real-time store prices.
  - Garnish and ice: listed as their own line items, not folded into the
    spirit/mixer totals, since they are commonly forgotten in manual
    planning.
  - A short plain-language purchase guide summarising what was combined
    across drinks (e.g. "Gin for these three drinks was combined into one
    purchase total") to make the shared-ingredient benefit visible to the
    user.
  - The web frontend presents every output bilingually (Chinese and
    English side by side), per the project's Stage 5 prototype design.

Budget mode descriptions (user-facing short text):
  - budget / 经济型: lowest reasonable cost using each base spirit's
    budget-tier SKU; every other ingredient stays at its one fixed
    value_default product.
  - standard / 平衡型 (default when the user does not state a tier): each
    base spirit's mid-tier SKU, still with every other ingredient at its
    fixed value_default product.
  - premium / 高端型: each base spirit's premium-tier SKU; costs more and
    may require reducing quantities if it exceeds the stated budget.
```

---
