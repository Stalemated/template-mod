package com.stalemated.templatemod.config;

import com.stalemated.lib.compat.yacl.builder.YaclCategoryBuilder;
import com.stalemated.lib.compat.yacl.builder.YaclScreenBuilder;
import com.stalemated.lib.config.ConfigManager;
import com.stalemated.templatemod.TemplateMod;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

public final class TemplateModConfigScreen {
    private TemplateModConfigScreen() {
    }

    public static Screen create(Screen parent) {
        return builder(parent, TemplateModConfigs.CONFIG).generateScreen();
    }

    static YaclScreenBuilder builder(Screen parent, ConfigManager<TemplateModConfig> config) {
        return YaclScreenBuilder.create(parent, Component.translatable("template_mod.config.title"), TemplateMod.MOD_ID)
                .category(config, "general", YaclCategoryBuilder::autoGenerate);
    }
}
