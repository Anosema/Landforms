# Landforms Generator

## Index
- [Prerequisite](https://github.com/Anosema/Landforms/Prerequisite)
- [Main Interface](https://github.com/Anosema/Landforms/Main-Interface)
	- [Grid Settings](https://github.com/Anosema/Landforms/Grid-Settings)
	- [Relief Settings](https://github.com/Anosema/Landforms/Relief-Settings)
	- [Tool Bar](https://github.com/Anosema/Landforms/Tool-Bar)
	- [Shortcuts](https://github.com/Anosema/Landforms/Shortcuts)
- [Config File](https://github.com/Anosema/Landforms/Config-File)
	- [Layer Mode](https://github.com/Anosema/Landforms/Layer-Mode)
	- [Landscape Mode](https://github.com/Anosema/Landforms/Landscape-Mode)

## Prerequisite
Make sure to have run `pip install -r requirements.txt` to install requiered modules

## Main Interface
### Grid Settings
- Precision : Step between two consecutive values multiplied by 100 (ex : 100 means only one value will be calculated between 1 and 2). Lower the precision get, heavier get the calculs
- Size : Size divided by 2 (ex : a size of 5 will give an area of 10\*10)
- The "Reset Grid" button will erase EVERY reliefs
- The "Reload Grid" button apply the change you did

### Relief Settings
- Height : the height of the peak of your new relief
- OffsetX : offset between (0, 0) and the (x,y) of the peak on X axis
- OffsetY : offset between (0, 0) and the (x,y) of the peak on Y axis
- Q : A weird thing, higher is the Q fatter is the peak
- The "Live Render" radio button will visualize the relief in real time, as you change it's settings. **IT CAN SLOW YOUR COMPUTER A LOT IF NOT POWERFUL ENOUGH**
- The "Visualize" button show you the plot with the actual relief without adding it to the plot, you can change it's settings
- The "Add Relief" button add the actual relief to the plot

### Tool Bar :
- Open File button to open a vaid txt plot save
- Export plot as a txt file or a litematic
- Undo button
- Redo button
- Add Relief button
- Reload Grid button
- Live Render button

### Shortcuts
- Ctrl+O : Open File
- Ctrl+E : Export File
- Ctrl+Z : Undo
- Ctrl+Y : Redo
- Ctrl+A : Add Relief
- Ctrl+R : Reload Grid
- Ctrl+L : Live Render

## Config File
You can choose which blocks will be used for the litematic file by editing the "config.json" file. By default, the config is as following
```json
{
	"isLayered": true,
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
	],
	"layer": [
		{"id":"minecraft:red_concrete"},
		{"id":"minecraft:orange_concrete"},
		{"id":"minecraft:blue_concrete"},
		{"id":"minecraft:green_concrete"}
	]
}
```

If `isLayered` is set to true the litematic will be in layer mode, otherwise it will be in landscape mode.

### Layer Mode
The list used to pick the blocks will be the `layer` one.
The top layer, in our exampe, will be the red concrete, and the bottom layer will be the green concrete.

### Landscape Mode :
The most top bock will be pick in the `soil` list, whie the other will be piced in the `underground` list.
The weight attribute is the percentage of chance the block associated will be picked.
The total weight of a list has to be == 100.


You can freely change this config file as long as it's still in a JSON format.
