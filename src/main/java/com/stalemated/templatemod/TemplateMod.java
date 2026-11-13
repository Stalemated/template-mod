package com.stalemated.templatemod;

import com.stalemated.templatemod.config.TemplateModConfigRegistry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

//? if fabric {
import net.fabricmc.api.ModInitializer;
//?} elif forge {
/*import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.loading.FMLEnvironment;
*///?} elif neoforge {
/*import net.neoforged.api.distmarker.Dist;
import net.neoforged.fml.common.Mod;
*///?}

//? if forge || neoforge {
/*@Mod(TemplateMod.MOD_ID)
*///?}
public final class TemplateMod //? if fabric
implements ModInitializer
{
    public static final String MOD_ID = "template_mod";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    //? if fabric {
    @Override
    public void onInitialize() {
        init();
    }
    //?} elif forge {
    /*public TemplateMod() {
        init();
        if (FMLEnvironment.dist == Dist.CLIENT) TemplateModClient.init();
    }
    *///?} elif neoforge {
    /*public TemplateMod(Dist dist) {
        init();
        if (dist == Dist.CLIENT) TemplateModClient.init();
    }
    *///?}

    private static void init() {
        TemplateModConfigRegistry.register();
    }
}
