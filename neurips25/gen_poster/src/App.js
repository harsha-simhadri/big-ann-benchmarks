import React from 'react';
import { BarChart, Search, Database, RefreshCw, Trophy, Users, Zap, Target } from 'lucide-react';
import './index.css';
import filtered from './filteredcomplete.jpg';
import qr from './qr2.jpg';
import fr from './filterresults.jpg';
import or from './oodresults.jpg';
import sr from './sparseresults.jpg';
import str from './streamingresults.jpg';

const BigAnnPoster = () => {
  return (
    <div className="w-full min-h-screen bg-gray-100 p-4 flex justify-center overflow-x-auto">
      {/* A0 Aspect Ratio Container (approx 1:1.414) */}
      {/* Using a fixed width scaling approach for viewing, but designed with A0 proportions */}
      <div 
        className="bg-white text-gray-900 shadow-2xl relative"
        style={{ 
          width: '4400px', // Scaled down for screen, but proportional
          minWidth: '4400px',
          //height: '1697px', 
          height: '3600px', 
          fontSize: '44px',
          fontFamily: '"Helvetica Neue", Helvetica, Arial, sans-serif',
          margin: '0px 0px 0x 0px'
        }}
      >      
        {/* Header Section */}
        <header className="bg-blue-900 text-white p-8 border-b-8 border-yellow-400">
          <div className="flex justify-between items-center mb-4">
            <div className="font-bold tracking-widest opacity-80">NeurIPS 2025 | SAN DIEGO</div>
            <div className="font-bold tracking-widest opacity-80">TRACK: BENCHMARKS AND DATASETS </div>
          </div>
          
          <h1 className="font-extrabold mb-6 leading-tight text-center">
            Results of the Big ANN: NeurIPS'23 Competition
          </h1>
          
          <div className="flex flex-wrap justify-center gap-x-8 gap-y-2 opacity-90 text-center px-12">
            <span>Harsha Vardhan Simhadri (Microsoft)</span>
            <span>Martin Aumüller (IT U. Copenhagen)</span>
            <span>Amir Ingber (Pinecone)</span>
            <span>Matthijs Douze (Meta AI)</span>
            <span>George Williams</span>
            <span>Dmitry Baranchuk (Yandex)</span>
            <span>Edo Liberty (Pinecone)</span>
            <span>Frank Liu (Zilliz)</span>
          </div>
          
          <div className="mt-6 text-center text-blue-200 italic">
            Participating Teams: Shanghai Jiao Tong University, Fudan University, Baidu, University of Maryland. and Carnegie Mellon University.
          </div>
        </header>

        {/* Main Content Grid - 3 Columns */}
        <div className="grid grid-cols-3 gap-8 p-8 h-[calc(100%-580px)]">
          
          {/* Column 1: Intro & Methodology */}
          <div className="flex flex-col gap-6">
            
            <section className="bg-gray-50 p-6 rounded-xl border-l-8 border-blue-600 shadow-sm">
              <h2 className="font-bold text-blue-800 mb-4 flex items-center gap-3">
                <Target size={32} /> Introduction
              </h2>
              <p className="leading-relaxed mb-4 text-justify">
                Approximate Nearest Neighbor (ANN) search is critical for LLMs (RAG), computer vision, and recommendation systems. While previous challenges focused on scaling standard dense vector indexing, the 2023 Big ANN Challenge[1] addressed <strong>practical, complex variants</strong> of ANN search encountered in real-world applications.
              </p>
              <div className="bg-blue-100 p-4 rounded-lg">
                <h3 className="font-bold text-blue-900 mb-2">Key Goals</h3>
                <ul className="list-disc ml-5 space-y-1 text-blue-900">
                  <li>Move beyond standard dense indexing.</li>
                  <li>Address diverse data distributions and types.</li>
                  <li>Evaluate on constrained hardware (16GB RAM).</li>
                  <li>Promote open-source contributions.</li>
                </ul>
              </div>
            </section>

            <section className="bg-gray-50 p-6 rounded-xl border-l-8 border-indigo-600 shadow-sm flex-grow">
              <h2 className="font-bold text-indigo-800 mb-4 flex items-center gap-3">
                <Database size={32} /> Tracks & Datasets
              </h2>
              
              <div className="space-y-6">
                <div className="border border-indigo-200 rounded-lg p-4 bg-white">
                  <h3 className="font-bold text-indigo-700 mb-2 flex items-center gap-2">
                    1. Filtered Search
                  </h3>
                  <div style={{
                            display: "flex"
                        }}
                  >
                    <div style={{ 
                            float: "left"
                        }}
                    >
                      <p className="mb-2 text-gray-600"><strong>Dataset:</strong> YFCC 100M[2] (CLIP embeddings + Tags)</p>
                      <p className="mb-2">Search for nearest neighbors that <em>also</em> match specific metadata tags.</p>
                    </div>
                    <div style={{ 
                            float: "left"
                        }}
                    >
                        <img src={filtered} alt="" width="1800"></img>
                    </div>
                    <div style={{
                            clear: "both"
                        }}
                    >
                    </div>
                  </div>
                </div>

                <div className="border border-indigo-200 rounded-lg p-4 bg-white">
                  <h3 className="font-bold text-indigo-700 mb-2 flex items-center gap-2">
                    2. Out-Of-Distribution (OOD)
                  </h3>
                  <p className="mb-2 text-gray-600"><strong>Dataset:</strong> Yandex Text-to-Image 10M [4]</p>
                  <p>Database (Images) and Query (Text) vectors have different distributions in the shared space. Standard indices often fail to provide high recall.</p>
                </div>

                <div className="border border-indigo-200 rounded-lg p-4 bg-white">
                  <h3 className="font-bold text-indigo-700 mb-2 flex items-center gap-2">
                    3. Sparse Search
                  </h3>
                  <p className="mb-2 text-gray-600"><strong>Dataset:</strong> MSMARCO[3] (SPLADE model)</p>
                  <p>High-dimensional vectors ({'>'}30k dim) with few non-zero elements (~120). Optimized for inverted indices and specialized graphs.</p>
                </div>

                <div className="border border-indigo-200 rounded-lg p-4 bg-white">
                  <h3 className="font-bold text-indigo-700 mb-2 flex items-center gap-2">
                    4. Streaming
                  </h3>
                  <p className="mb-2 text-gray-600"><strong>Dataset:</strong> MS Turing[4] (10M subset)</p>
                  <p>Indices must handle a "runbook" of Insertions, Deletions, and Searches under strict memory (8GB) and time limits.</p>
                </div>
              </div>
            </section>
          </div>

          {/* Column 2: Evaluation & Results Part 1 */}
          <div className="flex flex-col gap-6">
            
            <section className="bg-white p-6 rounded-xl border-t-8 border-gray-800 shadow-md">
              <h2 className="font-bold text-gray-800 mb-4 flex items-center gap-3">
                <Users size={32} /> Evaluation Protocol
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 p-3 rounded">
                  <span className="block font-bold text-gray-600">Hardware</span>
                  <span className="">Azure D8lds_v5</span>
                  <div className="text-gray-500">8 vCPUs, 16GB RAM</div>
                </div>
                <div className="bg-gray-50 p-3 rounded">
                  <span className="block font-bold text-gray-600">Metric</span>
                  <span className="">10-recall@10</span>
                  <div className="text-gray-500">& QPS (Throughput)</div>
                </div>
              </div>
              <p className="mt-4 italic text-gray-600 border-t pt-2">
                Ranking based on highest throughput (QPS) achieving at least 90% recall.  Streaming track used highest recall across searches.
              </p>
            </section>

            <section className="bg-green-50 p-6 rounded-xl border-l-8 border-green-600 shadow-sm flex-grow">
              <h2 className="font-bold text-green-800 mb-6 flex items-center gap-3">
                <Trophy size={32} /> Results & Winners
              </h2>

              <div className="mb-8">
                <div className="flex justify-between items-baseline mb-2 border-b border-green-200 pb-1">
                  <h3 className="font-bold text-green-900">Filtered Track</h3>
                  <span className="text-green-700 font-bold">Winner: ParlayANN</span>
                </div>
                <div style={{
                            display: "flex"
                        }} >
                  <div style={{
                                float: "left"
                            }} >
                    <div className="bg-white p-4 rounded shadow-sm">
                          <ul className="list-disc ml-5 space-y-2">
                            <li><strong>ParlayANN</strong> 11x baseline speed using inverted index for tags + Vamana graph for dense vectors. </li>
                          </ul>
                    </div>
                 </div>
                 <div style={{
                                margin: "0px 0px 0xp 0px",
                                float: "left"
                            }} > 
                            <img src={fr} alt="" width="3000"></img>
                 </div>
                 <div style={{
                            clear: "both"
                            }} >   
                 </div>
               </div>
                {/*
                  <div className="mt-4 h-32 bg-green-100 rounded flex items-center justify-center text-green-800 font-mono text-sm">
                    [Chart Placeholder: ParlayANN dominating QPS vs Recall curve]
                  </div>
                */}
              </div>

              <div className="mb-8">
                <div className="flex justify-between items-baseline mb-2 border-b border-green-200 pb-1">
                  <h3 className="font-bold text-green-900">OOD Track</h3>
                  <span className="text-green-700 font-bold">Winners: MysteryANN & PyANNS</span>
                </div>
                <div style={{
                            display: "flex"
                        }} >
                  <div style={{
                                float: "left"
                            }} >
                    <div className="bg-white p-4 rounded shadow-sm">
                      <ul className="list-disc ml-5 space-y-2">
                        <li><strong>MysteryANN:</strong> Bipartite graph between base and query samples to adapt the index.</li>
                        <li><strong>PyANNS:</strong> Relied on highly optimized Vamana graph + quantization.</li>
                      </ul>
                    </div>
                  </div>
                  <div style={{
                                margin: "0px 0px 0xp 0px",
                                float: "left"
                            }} >
                            <img src={or} alt="" width="445"></img>
                  </div>     
                  <div style={{
                            clear: "both"
                            }} >   
                  </div>
                </div>
              </div>
              
              <div className="mb-8">
                <div className="flex justify-between items-baseline mb-2 border-b border-green-200 pb-1">
                  <h3 className="font-bold text-green-900">Sparse Track</h3>
                  <span className="text-green-700 font-bold">Winners: PyANNS & GrassRMA</span>
                </div>
                <div style={{
                            display: "flex"
                        }} >
                  <div style={{
                                float: "left"
                            }} >
                    <div className="bg-white p-4 rounded shadow-sm">
                      <ul className="list-disc ml-5 space-y-2">
                        <li><strong>PyANNS:</strong> Quantized HNSW. Refinement step used full vectors to recover accuracy.</li>
                        <li><strong>GrassRMA:</strong> Optimized memory access patterns for sparse data in graphs.</li>
                      </ul>
                    </div>
                  </div>
                  <div style={{
                                margin: "0px 0px 0xp 0px",
                                float: "left"
                            }} >
                            <img src={sr} alt="" width="845"></img>
                  </div>
                  <div style={{
                            clear: "both"
                            }} >
                  </div>
                </div>
              </div>
              
              <div className="mb-4">
                <div className="flex justify-between items-baseline mb-2 border-b border-green-200 pb-1">
                  <h3 className="font-bold text-green-900">Streaming Track</h3>
                  <span className="text-green-700 font-bold">Winner: PyANNS</span>
                </div>

                <div style={{
                            backgroundColor: "white",
                            display: "flex"
                        }} >
                  <div style={{
                                float: "left"
                            }} >
                    <div className="bg-white p-4 rounded shadow-sm">
                      <ul className="list-disc ml-5 space-y-2">
                        <li><strong>PyANNS:</strong> Used DiskANN[4] strategy with 8-bit scalar quantization. Quantization allowed deeper graph search within the time limit, maintaining high recall despite deletions.</li>
                      </ul>
                    </div>
                  </div>
                  <div style={{
                                margin: "0px 0px 0xp 0px",
                                float: "left"
                            }} >
                            <img src={str} alt="" width="1600"></img>
                  </div> 
                  <div style={{
                            clear: "both"
                            }} >
                  </div>
                </div>
             </div>

            </section>
          </div>

          {/* Column 3: Results Part 2 & Conclusion */}
          <div className="flex flex-col gap-6">
            
            <section className="bg-yellow-50 p-6 rounded-xl border-t-8 border-yellow-400 shadow-lg flex-grow">
              <h2 className="font-bold text-yellow-800 mb-4 flex items-center gap-3">
                <Zap size={32} /> Discussion & Future Work
              </h2>
              <p className="mb-4 text-justify">
                The 2023 challenge demonstrated a significant leap in performance over industry baselines, driven by specialized data structures rather than raw scaling.
              </p>
              
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-white p-3 rounded border border-yellow-200">
                  <h4 className="font-bold text-yellow-900">Key Trends</h4>
                  <ul className="list-disc ml-4 text-gray-700">
                    <li><strong>Graph Indices</strong> are dominant, even for sparse/OOD.</li>
                    <li><strong>Quantization</strong> is essential for efficiency on constrained hardware.</li>
                    <li><strong>Hybrid Indices</strong> (Graph + Inverted) needed for Filtered search.</li>
                  </ul>
                </div>
                <div className="bg-white p-3 rounded border border-yellow-200">
                  <h4 className="font-bold text-yellow-900">Impact</h4>
                  <ul className="list-disc ml-4 text-gray-700">
                    <li>Established benchmarks for "ragged" real-world data.</li>
                    <li>Highlighted need for "deletions" support in streaming indices.</li>
                  </ul>
                </div>
              </div>
             
              <h2 className="font-bold text-yellow-800 mb-4 flex items-center gap-3">
                <Zap size={32} /> Github Repository
              </h2>
              <p className="mb-4 text-justify">
                  <div>
                    <div style={{
                            display: "flex"
                        }}
                    >
                        <div style={{ 
                                float: "left"
                            }}
                        >
                            We open-sourced the competition evaluation framework and all the participating algorithms.  Scan the QR Code and get detailed analysis, access to the algorithms, and more information about getting involved with future competitions!
                        </div>
                        <div style={{ 
                                margin: "0px 0px 0xp 100px",
                                float: "left"
                            }}
                        >
                            <img src={qr} alt="" width="3500"></img>
                        </div>
                        <div style={{
                            clear: "both"
                            }}
                        >
                        </div>
                    </div>
                  </div>
              </p>
              
              <div className="mt-auto pt-4 border-t border-yellow-200 text-gray-500">
                <strong>References:</strong>
                    <div>[1] Simhadri et al. "Results of the NeurIPS'21 Challenge on Billion-Sclae Approximate Nearest Neighbor Search." NeurIPS Competition and Demos, PMLR, 2021.
                    </div>
                    <div>[2] Thomee et al. "YFCC100M: The New Data in Multimedia Research" Comm. ACM, 2016.
                    </div>
                    <div>[3] Nguyen et al. "MS MARCO: A Human Generated Machine Reading Comprehension Dataset.", 2016.
                    </div>
                    <div>[4] Simhadri et al. "DiskANN: Graph-structured Indices for Scalable, Fast, Fresh and Filtered ANN Search", https://github.com/microsoft/DiskANN, 2023.
                    </div>
              </div>
            </section>
          </div>
        </div>

      </div>
    </div>
  );
};

export default BigAnnPoster;
