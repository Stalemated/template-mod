package com.stalemated.templatemod;

import com.stalemated.lib.client.SLibConfigScreens;
import com.stalemated.templatemod.config.TemplateModConfigScreen;

public final class TemplateModClient {
    private TemplateModClient() {
    }

    public static void init() {
        SLibConfigScreens.register(TemplateMod.MOD_ID, () -> TemplateModConfigScreen::create);
    }
}
