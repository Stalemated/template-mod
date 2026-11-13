package com.stalemated.templatemod.config;

import com.stalemated.lib.config.SLibConfig;
import com.stalemated.lib.config.SyncedConfigManager;
import com.stalemated.templatemod.TemplateMod;

public final class TemplateModConfigRegistry {
    public static final SyncedConfigManager<TemplateModConfig> CONFIG = SLibConfig.synced(TemplateMod.MOD_ID, TemplateModConfig.class).build();

    private TemplateModConfigRegistry() {
    }

    public static void register() {
        CONFIG.register();
    }
}
