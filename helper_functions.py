import matplotlib.pyplot as plt

def plot_distribution(df,field_name,figsize=(5,5),title=None):
	'''
	For a given dataframe, plot the distribution of the field.
	'''
	dist = df[field_name].value_counts()

	plt.figure(figsize=figsize)

	if(title is not None):
		plt.title(title)

	plt.barh(dist.index,dist.values)
	plt.show()
