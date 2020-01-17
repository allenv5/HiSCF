package cn.edu.whut.cslhu.tscag;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import org.apache.log4j.Logger;

public class HiSCF_Pruning {
	public static Logger logger = Logger.getLogger(HiSCF_Pruning.class);
	public static String DELIMITER = "\t";

	private String rootFolder;
	private String[] clusterFiles;
	private int[] sizeLimits;
	private float threshold;

	public HiSCF_Pruning(String rootFolder, String[] clusterFiles, int[] sizeLimits, float threshold) {
		this.rootFolder = rootFolder;
		this.clusterFiles = clusterFiles;
		this.sizeLimits = sizeLimits;
		this.threshold = threshold;
	}

	public void run() {
		Set<Set<String>> clusterSet = new HashSet<Set<String>>();
		
		for (int i = 0; i < clusterFiles.length; i++) {
			String clusterFile = this.rootFolder + File.separator + this.clusterFiles[i];
			int sizeLimit = this.sizeLimits[i];
			addToClusters(clusterSet, clusterFile, sizeLimit);
		}
		
		List<Set<String>> clusterList = sort(clusterSet);
		
		clusterList = pruningByNA(clusterList);
		
		save(clusterList);
	}

	private void save(List<Set<String>> clusterList) {
		// TODO Auto-generated method stub
		String content = "";
		
		for (int i = 0; i < clusterList.size(); i++) {
			content += i == 0 ? "" : "\n";
			
			String line = "";
			for (String item : clusterList.get(i))
				line += (line.length() == 0 ? "" : "\t") + item;
			
			content += line;
		}
		
		BufferedWriter bw = null;
		try {
			bw = new BufferedWriter(new FileWriter(rootFolder + File.separator + this.threshold+"-HiSFC.clusters"));
			bw.write(content);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			if (bw != null)
				try {
					bw.close();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
		}
	}

	private List<Set<String>> pruningByNA(List<Set<String>> clusters) {
		// TODO Auto-generated method stub
		Set<Integer> indicesToBePruned = new HashSet<>();
		
		for (int i = 0; i < clusters.size() - 1; i++) {
			if (indicesToBePruned.contains(i))
				continue;
			
			Set<String> cluster = clusters.get(i);
			
			for (int j = i + 1; j < clusters.size(); j++) {
				if (indicesToBePruned.contains(j))
					continue;
				
				Set<String> anotherCluster = clusters.get(j);
				if (neighboodAffinity(cluster, anotherCluster) >= this.threshold)
					indicesToBePruned.add(j);
			}
		}
		
		List<Set<String>> finalClusters = new ArrayList<Set<String>>();
		for (int i = 0; i < clusters.size(); i++) {
			if (indicesToBePruned.contains(i))
				continue;
			
			finalClusters.add(clusters.get(i));
		}
		
		return finalClusters;
	}

	private float neighboodAffinity(Set<String> cluster, Set<String> anotherCluster) {
		// TODO Auto-generated method stub
		int commonNum = 0;
		
		for (String item : cluster) {
			if (anotherCluster.contains(item))
				commonNum++;
		}
		
		return commonNum * commonNum / (float) (cluster.size() * anotherCluster.size());
	}

	private List<Set<String>> sort(Set<Set<String>> clusterSet) {
		// TODO Auto-generated method stub
		List<Set<String>> clusterList = clusterSet.stream().sorted(new Comparator<Set<String>>() {
            public int compare(Set<String> o1, Set<String> o2) {
            	return o2.size() - o1.size();
            }
        }).collect(Collectors.toList());
		
		return clusterList;
	}

	private void addToClusters(Set<Set<String>> clusters, String clusterFile, int sizeLimit) {
		// TODO Auto-generated method stub
		BufferedReader br;
		String line;
		
		try {
			br = new BufferedReader(new FileReader(clusterFile));
			while((line = br.readLine()) != null) {
				String[] items = line.split(DELIMITER);
				
				if (items.length < sizeLimit)
					continue;
				
				Set<String> cluster = new HashSet<String>();
				for (String item : items)
					cluster.add(item);
				clusters.add(cluster);
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		String rootFolder = "E:\\Workspace\\Julia\\GtensorSC\\data\\gcns\\unweighted\\arabidopsis";
		String[] clusterFiles = new String[]{"links-clusters", "tri-clusters"};
		int[] sizeLimits = new int[]{2,3};
		float threshold = 0.7f;
		
		HiSCF_Pruning app = new HiSCF_Pruning(rootFolder, clusterFiles, sizeLimits, threshold);
		app.run();
	}
}
