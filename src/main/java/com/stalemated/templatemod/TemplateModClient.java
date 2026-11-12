package com.stalemated.templatemod;

import com.stalemated.lib.client.SLibConfigScreens;
import com.stalemated.templatemod.config.TemplateModConfigScreen;

//? if fabric
import net.fabricmc.api.ClientModInitializer;

public final class TemplateModClient //? if fabric
implements ClientModInitializer
{
    //? if fabric {
    @Override
    public void onInitializeClient() {
        init();
    }
    //?} else {
    /*private TemplateModClient() {
    }
    *///?}

    static void init() {
        SLibConfigScreens.register(TemplateMod.MOD_ID, () -> TemplateModConfigScreen::create);
    }
}
