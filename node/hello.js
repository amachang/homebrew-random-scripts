#! /usr/bin/env node

import art from 'ascii-art'

art.font('Hello Node World!!', 'Doom', (err, rendered) => {
    console.log(rendered)
})

