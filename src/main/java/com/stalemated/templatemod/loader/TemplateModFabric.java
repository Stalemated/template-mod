package com.stalemated.templatemod.loader;

//? if fabric {
import com.stalemated.templatemod.TemplateMod;
import net.fabricmc.api.ModInitializer;

public final class TemplateModFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        TemplateMod.init();
    }
}
//?}
