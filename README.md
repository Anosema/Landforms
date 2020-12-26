# Landforms Generator

## Main Interface
### Grid Settings
- Precision : Step between two consecutive values multiplied by 100 (ex : 100 means only one value will be calculated between 1 and 2). Lower the precision get, heavier get the calculs;
- Size : Size divided by 2 (ex : a size of 5 will give an area of 10\*10)
- The "Reload Grid" button apply the change you did

### Relief Settings
- Height : the height of the peak of your new relief
- OffsetX : offset between (0, 0) and the (x,y) of the peak on X axis
- OffsetY : offset between (0, 0) and the (x,y) of the peak on Y axis
- Q : A weird thing, higher is the Q fatter is the peak.
- The "Visualize" button show you the plot with the actual relief without adding it to the plot, you can change his settings
- The "Add Relief" button ADD the actual relief to the plot, you **CANNOT CHANGE HIS SETTINGS**

## File Management
- You can open a saved by clicking "File" > "Open plot" and choosing a previously saved plot as txt
- You can export the plot as txt or as a litematic by clicking "File" > "Export" and choosing your option

## Config File
- You can choose which blocks will be used for the litematic file by editing the "config.json" file. By default, the config is as following
```
{
	"soil": [
		{"id":"minecraft:grass_block", "weight": 90},
		{"id":"minecraft:coarse_dirt", "weight": 5},
		{"id":"minecraft:podzol", "weight": 5}
	],
	"underground": [
		{"id":"minecraft:stone", "weight": 85},
		{"id":"minecraft:cobblestone", "weight": 5},
		{"id":"minecraft:andesite", "weight": 5},
		{"id":"minecraft:gravel", "weight": 5}
	]
}
```
"soil" is what will be used as floor, and "underground" is the blocks under the floor.
The weight is the percentage of blocks linked to it.
The total weight of a category has to be == 100
You can freely change this config file as long as it's still in a JSON format.