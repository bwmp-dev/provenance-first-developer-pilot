package dev.provenance.firstdev;

import org.bukkit.plugin.java.JavaPlugin;

public final class FirstDeveloperPilotPlugin extends JavaPlugin {
  @Override public void onEnable() {
    getLogger().info("PROVENANCE_FIRST_DEVELOPER_PILOT_FAILING_ON_PURPOSE");
    throw new IllegalStateException("Deliberate product failure fixture for failure classification");
  }
}
