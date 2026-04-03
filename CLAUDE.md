# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Odoo 19.0 website theme module** for dierenwinkelshop.be, deployed on **Odoo.sh**. Built using XML templates, SCSS, JavaScript, and QWeb.

## Odoo.sh Deployment Workflow

1. Push changes to the `main` branch on GitHub
2. Odoo.sh detects the push and triggers a rebuild automatically
3. If a build is stuck on an AI session, click **Rebuild** in the Odoo.sh dashboard
4. After rebuild: go to **Apps → Dierenwinkelshop → Upgrade** in the Odoo backend
5. **Rebuild alone is not enough** — you must also upgrade the module for XML/template changes to apply

## Module Structure

```
website_dierenwinkelshop/
├── __init__.py
├── __manifest__.py
├── i18n/                         # Translation files (.po)
├── data/
│   ├── presets.xml               # Activate/deactivate Odoo views
│   ├── website.xml               # Website name, logo, favicon
│   ├── images.xml                # Media library images
│   ├── gradients.xml             # Custom gradient presets
│   ├── shapes.xml                # Custom SVG background shapes
│   └── pages/                   # Page definitions (home.xml, contact.xml, etc.)
├── views/
│   ├── website_templates.xml     # Header, footer, general layout
│   ├── website_sale_templates.xml # Shop and product page overrides
│   └── snippets/
│       ├── options.xml           # Register custom snippets in Website Builder
│       └── s_<snippet_name>.xml  # Per-snippet templates
└── static/src/
    ├── scss/
    │   ├── primary_variables.scss      # Odoo-specific variables (colors, fonts)
    │   ├── bootstrap_overridden.scss   # Bootstrap variable overrides
    │   ├── theme.scss                  # General custom SCSS
    │   ├── layout/                     # header.scss, footer.scss
    │   ├── components/                 # Reusable UI components
    │   ├── snippets/                   # Per-snippet SCSS
    │   └── pages/                      # Page-specific SCSS (shop.scss, product_page.scss)
    ├── js/                             # Custom JavaScript
    └── img/
        ├── content/                    # Images, icons, branding
        ├── snippets/                   # Snippet preview images
        └── wbuilder/                   # Website Builder thumbnails
```

## Key Development Patterns

### SCSS Variable Priority
1. `primary_variables.scss` — Odoo theme variables (colors, font families)
2. `bootstrap_overridden.scss` — Bootstrap variable overrides (typography, inputs, buttons)
3. `theme.scss` / component files — Custom rules

Always wrap custom SCSS rules inside `#wrapwrap` to scope them to the website only.

### Declaring Assets in `__manifest__.py`
All SCSS and JS files must be declared under `assets`, all XML files under `data`:
```python
'assets': {
    'web.assets_frontend': [
        'website_dierenwinkelshop/static/src/scss/primary_variables.scss',
        'website_dierenwinkelshop/static/src/scss/bootstrap_overridden.scss',
        'website_dierenwinkelshop/static/src/scss/theme.scss',
    ],
},
'data': [
    'data/presets.xml',
    'views/snippets/s_mysnippet.xml',
    'views/snippets/options.xml',
],
```

### Custom Building Blocks (Snippets) — Verified Working in Odoo 19

Registration in `views/snippets/options.xml` requires **two XPath steps**:

```xml
<template id="snippets" inherit_id="website.snippets" name="My Snippets">

    <!-- Step 1: Create a custom group tab in the snippet panel -->
    <xpath expr="//snippets[@id='snippet_groups']/*[1]" position="before">
        <t snippet-group="mygroupname"
           t-snippet="website.s_snippet_group"
           string="My Group Label"/>
    </xpath>

    <!-- Step 2: Register snippets under that group -->
    <xpath expr="//snippets[@id='snippet_structure']/*[1]" position="before">
        <t t-snippet="module_name.s_mysnippet"
           string="My Snippet"
           group="mygroupname">
            <keywords>search keywords here</keywords>
        </t>
    </xpath>

</template>
```

- `group` (singular) links the snippet to the group — do NOT use `groups` (plural, that is for access rights)
- The custom group tab appears at the top of the blocks panel in the Website Builder
- After pushing changes, always **upgrade the module** — a rebuild alone does not apply template changes

### QWeb Template Rules (Odoo 19)

**Do NOT use Python builtins in QWeb expressions.** These will cause a `KeyError` at render time:
```xml
<!-- WRONG — hasattr is not available in QWeb -->
<header t-attf-class="#{' overlay' if hasattr(obj, 'field') and obj.field else ''}"/>

<!-- CORRECT — use safe attribute access -->
<header t-attf-class="#{' overlay' if main_object and main_object.get('field') else ''}"/>
```

### Extending eCommerce Templates (Odoo 19)

XPaths that existed in older Odoo versions no longer work in Odoo 19. Always verify XPaths exist before using them. Known broken XPaths:
- `//t[@t-set='columns']` in `website_sale.products` — does not exist in Odoo 19
- `//div[hasclass('css_quantity')]` in `website_sale.product` — does not exist in Odoo 19

When unsure, inspect the live template in Odoo's developer mode before writing XPath overrides.

### Presets (`data/presets.xml`)
Enable or disable built-in Odoo views:
```xml
<record id="website.template_header_default" model="ir.ui.view">
    <field name="active" eval="False"/>
</record>
```

### Page Templates (`data/pages/*.xml`)
Use `noupdate="1"` on page and navigation records to protect client edits during upgrades.

### Extending Odoo Templates
Organize overrides by area:
- General layout → `website_templates.xml`
- eCommerce → `website_sale_templates.xml`
- Blog → `website_blog_templates.xml`

### Custom Background Shapes
- Use colors from Odoo's **default palette** in SVG files — Odoo maps them at render time
- Use `illustration/` prefix in class names for custom shapes (not `web_editor/`)

### Animations
Classes: `o_animate`, `o_anim_fade_in`, `o_anim_zoom_out`, `o_anim_rotate_in`, `o_anim_from_bottom`
Timing: `animation-delay` style and `--wanim-intensity` CSS variable

### Translations
Export `.po` files from the backend, place in `i18n/`. Must be manually imported after installation on a new database.

## Dependencies

- `website_sale` — eCommerce/shop
- `website_sale_wishlist` — wishlist
- `website_blog` — blog
- `website_mass_mailing` — newsletter (only add when actively using it)
