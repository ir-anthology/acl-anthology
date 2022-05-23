Some venues are greyed out on the index page, even though this event did happen.

This is to emphasize, that there is no data available. But this is marked manually, and not extracted from the data.

Remove a greyed-out year in the file `hugo/layouts/index.html`. There is a variable `$event_exists_but_not_index`. It contains all years that are greyed out. Removing one item makes it clickable.