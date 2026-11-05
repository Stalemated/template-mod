package com.stalemated.templatemod.mixin;

import com.stalemated.templatemod.TemplateMod;
import net.minecraft.server.MinecraftServer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(MinecraftServer.class)
public abstract class MinecraftServerMixin {
    @Inject(method = "loadLevel", at = @At("HEAD"))
    private void template_mod$logLevelLoad(CallbackInfo ci) {
        TemplateMod.LOGGER.info("{} sees the level loading", TemplateMod.MOD_ID);
    }
}
