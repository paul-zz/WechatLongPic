        draw = ImageDraw.Draw(rendered_img)
        caption_size = draw.textsize(self.caption_text, self.caption_font)
        subtitle_size = draw.textsize(self.subtitle_text, self.subtitle_font)
        caption_x = self.size // 2 - caption_size[0] // 2
        caption_y = self.size // 2 - caption_size[1] - self.caption_offset
        subtitle_x = self.size // 2 - subtitle_size[0] // 2
        subtitle_y = self.size // 2 + self.caption_offset
        draw.text((caption_x, caption_y), self.caption_text, self.caption_color, font=self.caption_font)
        draw.text((subtitle_x, subtitle_y), self.subtitle_text, self.subtitle_color, font=self.subtitle_font)