package com.stalemated.templatemod.loader;

//? if forge {
/*import com.stalemated.templatemod.TemplateMod;
import com.stalemated.templatemod.TemplateModClient;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.loading.FMLEnvironment;

@Mod(TemplateMod.MOD_ID)
public final class TemplateModForge {
    public TemplateModForge() {
        TemplateMod.init();
        if (FMLEnvironment.dist == Dist.CLIENT) {
            TemplateModClient.init();
        }
    }
}
*///?}
