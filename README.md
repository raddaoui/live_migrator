# live_migrator
Live migration benchmark toolset for contionus LM testing

### usage
to use this live migration plugin

	git clone https://github.com/osic/live_migrator.git
	cd live_migrator
	rally --plugin-paths nova_live_migration.py task start task.json --task-args '{"image_name": "Ubuntu 14.04 LTS", "flavor_name": "test.large"}'
