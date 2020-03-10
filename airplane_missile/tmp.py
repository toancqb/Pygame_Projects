
        player = Player(self.move_up_sound, self.move_down_sound)
        # Create groups to hold enemy sprites, cloud sprites, and all sprites
        # - enemies is used for collision detection and position updates
        # - clouds is used for position updates
        # - all_sprites is used for rendering
        enemies = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
                elif event.type == self.ADDENEMY:
                    new_enemy = Enemy()
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
                elif event.type == self.ADDBOSS:
                    new_boss = Boss()
                    enemies.add(new_boss)
                    all_sprites.add(new_boss)
                elif event.type == self.ADDCLOUD:
                    new_cloud = Cloud()
                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)

            pressed_keys = pygame.key.get_pressed()

            player.update(pressed_keys)
            enemies.update()
            clouds.update()

            self.screen.fill(BLUE)

            #screen.blit(player.surf, player.rect)
            for entity in all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            if pygame.sprite.spritecollideany(player, enemies):
                self.move_up_sound.stop()
                self.move_down_sound.stop()
                self.collision_sound.play()
                player.kill()
                running = False

            txt = font.render("SCORE "+str(SCORE), True, GREEN)
            self.screen.blit(txt, (5, 5))
            pygame.display.flip()
            self.clock.tick(30)
