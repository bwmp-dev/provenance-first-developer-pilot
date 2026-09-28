package dev.provenance.firstdev;

import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.plugin.java.JavaPlugin;

public final class FirstDeveloperPilotPlugin extends JavaPlugin {
  @Override public void onEnable() {
    getLogger().info("PROVENANCE_FIRST_DEVELOPER_PILOT_READY");
  }
  @Override public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
    if (!label.equalsIgnoreCase("firstdevpilot") || args.length != 0) return false;
    sender.sendMessage("PROVENANCE_FIRST_DEVELOPER_PILOT_PASSED");
    getLogger().info("PROVENANCE_FIRST_DEVELOPER_PILOT_PASSED");
    return true;
  }
}
