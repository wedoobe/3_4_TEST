# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Odoo 19.0 website theme module**. It follows the standard Odoo module pattern and is built using XML templates, SCSS, JavaScript, and QWeb.

## Running the Theme

```bash
./odoo-bin --addons-path=../enterprise,addons,../myprojects \
  --db-filter=<db_name> \
  -d <db_name> \
  --without-demo=all \
  -i <module_name> \
  --dev=xml
```

Use `--dev=xml` during development to reload XML without restarting. Restart the server when changing SCSS variables.

## Module Structure

```
<module_name>/
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
│   ├── new_page_template_templates.xml
│   └── snippets/
│       ├── options.xml           # Register custom snippets in Website Builder
│       └── s_<snippet_name>.xml  # Per-snippet templates and options
└── static/src/
    ├── scss/
    │   ├── primary_variables.scss      # Odoo-specific variables (colors, fonts, templates)
    │   ├── bootstrap_overridden.scss   # Bootstrap variable overrides
    │   ├── theme.scss                  # General custom SCSS
    │   ├── layout/                     # header.scss, footer.scss
    │   ├── components/                 # Reusable UI components
    │   ├── snippets/                   # Per-snippet SCSS
    │   └── pages/                      # Page-specific SCSS (shop.scss, product_page.scss)
    ├── js/                             # Custom JavaScript
    ├── img/
    │   ├── content/                    # Images, icons, branding
    │   ├── snippets/                   # Snippet preview images
    │   └── wbuilder/                   # Website Builder thumbnails/illustrations
    └── snippets/
        └── s_<snippet_name>/
            └── 000.scss
```

## Key Development Patterns

### SCSS Variable Priority
1. `primary_variables.scss` — Odoo theme variables (colors, font families, header/footer template choice)
2. `bootstrap_overridden.scss` — Bootstrap v4.6 variable overrides (typography scale, input styles, etc.)
3. `theme.scss` / component files — Custom rules

Always wrap custom SCSS rules inside `#wrapwrap` to scope them to the website only (excludes backend).

### Declaring Assets in `__manifest__.py`
All SCSS and JS files must be declared under `assets`:
```python
'assets': {
    'web.assets_frontend': [
        'module_name/static/src/scss/primary_variables.scss',
        'module_name/static/src/scss/bootstrap_overridden.scss',
        'module_name/static/src/scss/theme.scss',
        'module_name/static/src/js/my_script.js',
    ],
}
```
All XML files must be declared under `data`. New page templates also need a `new_page_templates` key.

### Presets (`data/presets.xml`)
Enable or disable built-in Odoo views using `ir.ui.view` records:
```xml
<record id="website.template_header_default" model="ir.ui.view">
    <field name="active" eval="False"/>
</record>
```

### Page Templates (`data/pages/*.xml`)
Pages use `website.page` records with QWeb `arch`. Always call `website.layout` and set `additional_title`. Use `noupdate="1"` on navigation and page records to protect client edits during module updates.

### Extending Odoo Templates
Use XPath to extend existing Odoo views. Organize overrides by area:
- General layout → `website_templates.xml`
- eCommerce → `website_sale_templates.xml`
- Blog → `website_blog_templates.xml`

### Custom Building Blocks (Snippets)
1. Create the snippet template XML in `views/snippets/s_<name>.xml`
2. Register it in the Website Builder via XPath on `website.snippets` in `views/snippets/options.xml`
3. Add snippet options (`we-button-group`, `we-range`, etc.) by extending `website.snippet_options`
4. Place SCSS in `static/src/snippets/s_<name>/000.scss`

### Custom Background Shapes
- Shape files are SVGs placed in `static/src/img/`
- In SVG files, use colors from Odoo's **default palette** (not your theme colors) — Odoo maps them at render time
- When applying a custom shape to a section, use `illustration/` prefix in the class instead of `web_editor/`

### Gradients
Add custom gradients to the Website Builder colorpicker by inheriting `web_editor.colorpicker` and appending to the `gradients` t-set list.

### Animations
Use Odoo animation classes on elements: `o_animate`, `o_anim_fade_in`, `o_anim_zoom_out`, `o_anim_rotate_in`, `o_anim_from_bottom`. Control timing with `animation-delay` and `--wanim-intensity` CSS variables.

### Dynamic Snippets
Custom templates for dynamic snippets (e.g., product carousels) are registered in `views/snippets/options.xml` and must match the key referenced in the page XML `data-template-key`.

### eCommerce Pages
Shop and product pages are auto-generated by `website_sale`. Customize them exclusively via XPath, presets, and SCSS — never copy-paste the full template.

### Translations
Export `.po` files from the backend and place them in `i18n/`. Translations must be manually imported after module installation on a new database.

## Dependencies

Common modules to add to `depends` as features are added:
- `website` — always required
- `website_sale` — eCommerce/shop
- `website_sale_wishlist` — wishlist feature
- `website_blog` — blog
- `website_mass_mailing` — newsletter/footer subscription

## Deployment

Before importing to a client SaaS database:
- Ensure `base_import_module` is installed on the target database
- Verify all dependency modules are installed
- Manually import translation `.po` files after installation
